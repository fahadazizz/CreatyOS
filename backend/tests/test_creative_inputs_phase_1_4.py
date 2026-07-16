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
        "/api/v1/workspaces", json={"name": "Ingestion Studio", "slug": "ingestion-studio"}
    )
    user = await client.post(
        "/api/v1/users",
        json={"email": "input-owner@example.com", "display_name": "Input Owner"},
    )
    project = await client.post(
        "/api/v1/projects",
        json={
            "workspace_id": workspace.json()["id"],
            "owner_user_id": user.json()["id"],
            "title": "Input Film",
        },
    )
    return project.json()["id"], user.json()["id"]


@pytest.mark.anyio
async def test_store_script_as_candidate_input_not_artifact(client: httpx.AsyncClient) -> None:
    project_id, user_id = await _project_context(client)

    creative_input = await client.post(
        f"/api/v1/projects/{project_id}/creative-inputs",
        json={
            "submitted_by_user_id": user_id,
            "input_type": "script",
            "title": "Submitted Script",
            "source_label": "client draft",
            "body": {
                "raw_text": "Opening narration that must not become timeline truth.",
                "format": "text/plain",
            },
        },
    )

    assert creative_input.status_code == 201
    assert creative_input.json()["input_type"] == "script"
    assert creative_input.json()["candidate_state"] == "candidate"

    artifacts = await client.get(f"/api/v1/projects/{project_id}/artifacts")
    assert artifacts.status_code == 200
    assert artifacts.json() == []

    invalid_artifact = await client.post(
        f"/api/v1/projects/{project_id}/artifacts",
        json={
            "owner_user_id": user_id,
            "artifact_type": "script",
            "title": "Script Artifact",
        },
    )
    assert invalid_artifact.status_code == 422


@pytest.mark.anyio
async def test_list_get_and_filter_creative_inputs(client: httpx.AsyncClient) -> None:
    project_id, user_id = await _project_context(client)

    script_input = await client.post(
        f"/api/v1/projects/{project_id}/creative-inputs",
        json={
            "submitted_by_user_id": user_id,
            "input_type": "script",
            "title": "Script",
            "body": {"raw_text": "Script candidate"},
        },
    )
    brief_input = await client.post(
        f"/api/v1/projects/{project_id}/creative-inputs",
        json={
            "submitted_by_user_id": user_id,
            "input_type": "raw_brief",
            "title": "Brief",
            "body": {"raw_text": "Brief candidate"},
        },
    )
    assert script_input.status_code == 201
    assert brief_input.status_code == 201

    listed = await client.get(f"/api/v1/projects/{project_id}/creative-inputs")
    assert listed.status_code == 200
    assert [item["input_type"] for item in listed.json()] == ["script", "raw_brief"]

    filtered = await client.get(
        f"/api/v1/projects/{project_id}/creative-inputs?input_type=raw_brief"
    )
    assert filtered.status_code == 200
    assert [item["id"] for item in filtered.json()] == [brief_input.json()["id"]]

    fetched = await client.get(f"/api/v1/creative-inputs/{script_input.json()['id']}")
    assert fetched.status_code == 200
    assert fetched.json()["body"]["raw_text"] == "Script candidate"


@pytest.mark.anyio
async def test_creative_input_validation_and_audit(client: httpx.AsyncClient) -> None:
    project_id, user_id = await _project_context(client)

    invalid = await client.post(
        f"/api/v1/projects/{project_id}/creative-inputs",
        json={
            "submitted_by_user_id": user_id,
            "input_type": "raw_brief",
            "title": "Empty Brief",
            "body": {},
        },
    )
    assert invalid.status_code == 422

    created = await client.post(
        f"/api/v1/projects/{project_id}/creative-inputs",
        json={
            "submitted_by_user_id": user_id,
            "input_type": "reference",
            "title": "Reference",
            "body": {"url": "https://example.invalid/reference", "reason": "visual restraint"},
        },
    )
    assert created.status_code == 201

    audit_events = await client.get(f"/api/v1/audit-events?project_id={project_id}")
    assert audit_events.status_code == 200
    input_events = [
        (event["entity_type"], event["action"]) for event in audit_events.json()
    ]
    assert ("creative_input", "created") in input_events
