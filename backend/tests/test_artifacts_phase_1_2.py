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
        "/api/v1/workspaces", json={"name": "Living Film Studio", "slug": "living-film"}
    )
    assert workspace.status_code == 201
    user = await client.post(
        "/api/v1/users",
        json={"email": "owner@example.com", "display_name": "Artifact Owner"},
    )
    assert user.status_code == 201
    project = await client.post(
        "/api/v1/projects",
        json={
            "workspace_id": workspace.json()["id"],
            "owner_user_id": user.json()["id"],
            "title": "Foundation Film",
        },
    )
    assert project.status_code == 201
    return project.json()["id"], user.json()["id"]


@pytest.mark.anyio
async def test_create_artifact_and_append_only_versions(client: httpx.AsyncClient) -> None:
    project_id, user_id = await _project_context(client)

    artifact = await client.post(
        f"/api/v1/projects/{project_id}/artifacts",
        json={
            "owner_user_id": user_id,
            "artifact_type": "creative_problem",
            "title": "Creative Problem",
        },
    )
    assert artifact.status_code == 201
    artifact_id = artifact.json()["id"]

    first_version = await client.post(
        f"/api/v1/artifacts/{artifact_id}/versions",
        json={
            "schema_version": "creative_problem.v1",
            "author_user_id": user_id,
            "confidence_level": "medium",
            "body": {
                "audience": "curious founders",
                "objective": "show the strategic cost of generic AI video",
            },
            "linked_decisions": [],
            "linked_evidence": ["brief:founder-interview"],
            "open_questions": ["What example best proves the risk?"],
        },
    )
    assert first_version.status_code == 201
    assert first_version.json()["version_number"] == 1
    assert first_version.json()["schema_version"] == "creative_problem.v1"

    second_version = await client.post(
        f"/api/v1/artifacts/{artifact_id}/versions",
        json={
            "schema_version": "creative_problem.v1",
            "author_user_id": user_id,
            "parent_version_id": first_version.json()["id"],
            "confidence_level": "high",
            "body": {
                "audience": "creative founders",
                "objective": "prove direction beats media assembly",
            },
            "linked_decisions": [],
            "linked_evidence": ["brief:founder-interview", "source:reference-architecture"],
            "open_questions": [],
        },
    )
    assert second_version.status_code == 201
    assert second_version.json()["version_number"] == 2

    versions = await client.get(f"/api/v1/artifacts/{artifact_id}/versions")
    assert versions.status_code == 200
    assert [version["version_number"] for version in versions.json()] == [1, 2]
    assert versions.json()[0]["body"]["objective"] == "show the strategic cost of generic AI video"
    assert versions.json()[1]["body"]["objective"] == "prove direction beats media assembly"


@pytest.mark.anyio
async def test_artifact_type_and_version_body_are_validated(client: httpx.AsyncClient) -> None:
    project_id, user_id = await _project_context(client)

    invalid_artifact = await client.post(
        f"/api/v1/projects/{project_id}/artifacts",
        json={
            "owner_user_id": user_id,
            "artifact_type": "script",
            "title": "Script As Truth",
        },
    )
    assert invalid_artifact.status_code == 422

    artifact = await client.post(
        f"/api/v1/projects/{project_id}/artifacts",
        json={
            "owner_user_id": user_id,
            "artifact_type": "audience_experience",
            "title": "Audience Experience",
        },
    )
    assert artifact.status_code == 201

    invalid_version = await client.post(
        f"/api/v1/artifacts/{artifact.json()['id']}/versions",
        json={
            "schema_version": "audience_experience.v1",
            "author_user_id": user_id,
            "confidence_level": "medium",
            "body": {},
        },
    )
    assert invalid_version.status_code == 422


@pytest.mark.anyio
async def test_artifact_version_writes_audit_event(client: httpx.AsyncClient) -> None:
    project_id, user_id = await _project_context(client)
    artifact = await client.post(
        f"/api/v1/projects/{project_id}/artifacts",
        json={
            "owner_user_id": user_id,
            "artifact_type": "risk_register",
            "title": "Risk Register",
        },
    )
    version = await client.post(
        f"/api/v1/artifacts/{artifact.json()['id']}/versions",
        json={
            "schema_version": "risk_register.v1",
            "author_user_id": user_id,
            "confidence_level": "low",
            "body": {"risks": ["generic visual fallback"]},
            "open_questions": ["What proof should retire this risk?"],
        },
    )
    assert version.status_code == 201

    audit_events = await client.get(f"/api/v1/audit-events?project_id={project_id}")
    assert audit_events.status_code == 200
    artifact_events = [
        (event["entity_type"], event["action"]) for event in audit_events.json()
    ]
    assert ("artifact", "created") in artifact_events
    assert ("artifact_version", "created") in artifact_events
