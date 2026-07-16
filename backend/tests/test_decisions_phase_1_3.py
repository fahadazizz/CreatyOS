from collections.abc import AsyncGenerator

import httpx
import pytest
from sqlalchemy.orm import Session, sessionmaker

from app import models  # noqa: F401
from app.db import Base, get_db, make_engine
from app.main import create_app


@pytest.fixture()
def anyio_backend() -> str:
    return "asyncio"


@pytest.fixture()
async def client() -> AsyncGenerator[httpx.AsyncClient, None]:
    engine = make_engine("sqlite+pysqlite:///:memory:")
    TestingSessionLocal = sessionmaker(
        bind=engine, autoflush=False, autocommit=False, expire_on_commit=False
    )
    Base.metadata.create_all(bind=engine)

    app = create_app()

    async def override_db() -> AsyncGenerator[Session, None]:
        db = TestingSessionLocal()
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_db

    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url="http://testserver") as test_client:
        yield test_client


async def _project_context(client: httpx.AsyncClient) -> tuple[str, str]:
    workspace = await client.post(
        "/api/v1/workspaces", json={"name": "Decision Studio", "slug": "decision-studio"}
    )
    user = await client.post(
        "/api/v1/users",
        json={"email": "decision-owner@example.com", "display_name": "Decision Owner"},
    )
    project = await client.post(
        "/api/v1/projects",
        json={
            "workspace_id": workspace.json()["id"],
            "owner_user_id": user.json()["id"],
            "title": "Decision Film",
        },
    )
    return project.json()["id"], user.json()["id"]


async def _artifact_with_version(client: httpx.AsyncClient) -> tuple[str, str, str, str]:
    project_id, user_id = await _project_context(client)
    artifact = await client.post(
        f"/api/v1/projects/{project_id}/artifacts",
        json={
            "owner_user_id": user_id,
            "artifact_type": "creative_problem",
            "title": "Creative Problem",
        },
    )
    version = await client.post(
        f"/api/v1/artifacts/{artifact.json()['id']}/versions",
        json={
            "schema_version": "creative_problem.v1",
            "author_user_id": user_id,
            "confidence_level": "medium",
            "body": {"objective": "choose the most defensible route"},
        },
    )
    return project_id, user_id, artifact.json()["id"], version.json()["id"]


def _decision_payload(user_id: str, artifact_id: str, version_id: str) -> dict:
    return {
        "owner_user_id": user_id,
        "target_artifact_id": artifact_id,
        "target_artifact_version_id": version_id,
        "title": "Select operating thesis",
        "decision_text": "Choose the route that makes creative direction the product.",
        "alternatives_considered": [
            "Direction-first operating system",
            "Script-to-video assembly pipeline",
        ],
        "selected_option": "Direction-first operating system",
        "rationale": "It preserves authorship and source-of-truth boundaries.",
        "evidence": ["docs:reference-architecture", "docs:product-doctrine"],
        "risks": ["Requires more upfront modeling than media assembly."],
        "affected_scope": {
            "artifacts": [artifact_id],
            "versions": [version_id],
            "downstream": ["Living Film Model", "artifact contracts"],
        },
    }


@pytest.mark.anyio
async def test_create_list_and_get_decision(client: httpx.AsyncClient) -> None:
    project_id, user_id, artifact_id, version_id = await _artifact_with_version(client)

    created = await client.post(
        f"/api/v1/projects/{project_id}/decisions",
        json=_decision_payload(user_id, artifact_id, version_id),
    )
    assert created.status_code == 201
    assert created.json()["status"] == "proposed"
    assert created.json()["alternatives_considered"] == [
        "Direction-first operating system",
        "Script-to-video assembly pipeline",
    ]

    listed = await client.get(f"/api/v1/projects/{project_id}/decisions")
    assert listed.status_code == 200
    assert [decision["id"] for decision in listed.json()] == [created.json()["id"]]

    fetched = await client.get(f"/api/v1/decisions/{created.json()['id']}")
    assert fetched.status_code == 200
    assert fetched.json()["rationale"] == "It preserves authorship and source-of-truth boundaries."


@pytest.mark.anyio
async def test_decision_validation_requires_selected_alternative(
    client: httpx.AsyncClient,
) -> None:
    project_id, user_id, artifact_id, version_id = await _artifact_with_version(client)
    payload = _decision_payload(user_id, artifact_id, version_id)
    payload["selected_option"] = "A third unsupported option"

    response = await client.post(f"/api/v1/projects/{project_id}/decisions", json=payload)

    assert response.status_code == 422


@pytest.mark.anyio
async def test_decision_status_change_writes_audit_event(client: httpx.AsyncClient) -> None:
    project_id, user_id, artifact_id, version_id = await _artifact_with_version(client)
    created = await client.post(
        f"/api/v1/projects/{project_id}/decisions",
        json=_decision_payload(user_id, artifact_id, version_id),
    )

    updated = await client.patch(
        f"/api/v1/decisions/{created.json()['id']}/status",
        json={"status": "accepted"},
    )
    assert updated.status_code == 200
    assert updated.json()["status"] == "accepted"

    audit_events = await client.get(f"/api/v1/audit-events?project_id={project_id}")
    assert audit_events.status_code == 200
    decision_events = [
        (event["entity_type"], event["action"]) for event in audit_events.json()
    ]
    assert ("decision", "created") in decision_events
    assert ("decision", "status_changed") in decision_events


@pytest.mark.anyio
async def test_artifact_version_linked_decisions_must_exist(
    client: httpx.AsyncClient,
) -> None:
    project_id, user_id, artifact_id, version_id = await _artifact_with_version(client)
    decision = await client.post(
        f"/api/v1/projects/{project_id}/decisions",
        json=_decision_payload(user_id, artifact_id, version_id),
    )
    assert decision.status_code == 201

    valid_version = await client.post(
        f"/api/v1/artifacts/{artifact_id}/versions",
        json={
            "schema_version": "creative_problem.v1",
            "author_user_id": user_id,
            "confidence_level": "high",
            "body": {"objective": "record decision-linked source of truth"},
            "linked_decisions": [decision.json()["id"]],
        },
    )
    assert valid_version.status_code == 201
    assert valid_version.json()["linked_decisions"] == [decision.json()["id"]]

    invalid_version = await client.post(
        f"/api/v1/artifacts/{artifact_id}/versions",
        json={
            "schema_version": "creative_problem.v1",
            "author_user_id": user_id,
            "confidence_level": "high",
            "body": {"objective": "invalid decision link"},
            "linked_decisions": ["00000000-0000-0000-0000-000000000099"],
        },
    )
    assert invalid_version.status_code == 404
