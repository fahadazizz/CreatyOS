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


@pytest.mark.anyio
async def test_create_project_hierarchy_writes_audit_events(client: httpx.AsyncClient) -> None:
    workspace = await client.post(
        "/api/v1/workspaces", json={"name": "Editorial Studio", "slug": "editorial-studio"}
    )
    assert workspace.status_code == 201

    user = await client.post(
        "/api/v1/users",
        json={"email": "director@example.com", "display_name": "Creative Director"},
    )
    assert user.status_code == 201

    project = await client.post(
        "/api/v1/projects",
        json={
            "workspace_id": workspace.json()["id"],
            "owner_user_id": user.json()["id"],
            "title": "Documentary Pilot",
            "logline": "A premium editorial pilot.",
        },
    )
    assert project.status_code == 201
    project_id = project.json()["id"]

    production = await client.post(
        f"/api/v1/projects/{project_id}/productions",
        json={"title": "Episode 1", "format": "premium-editorial-documentary"},
    )
    assert production.status_code == 201

    piece = await client.post(
        f"/api/v1/productions/{production.json()['id']}/pieces",
        json={"title": "Main Film", "runtime_target_seconds": 600},
    )
    assert piece.status_code == 201

    deliverable = await client.post(
        f"/api/v1/pieces/{piece.json()['id']}/deliverables",
        json={"name": "YouTube Master", "platform": "youtube", "delivery_format": "16:9"},
    )
    assert deliverable.status_code == 201

    audit_events = await client.get(f"/api/v1/audit-events?project_id={project_id}")
    assert audit_events.status_code == 200
    actions = [(event["entity_type"], event["action"]) for event in audit_events.json()]
    assert actions == [
        ("project", "created"),
        ("production", "created"),
        ("piece", "created"),
        ("deliverable", "created"),
    ]


@pytest.mark.anyio
async def test_project_requires_existing_workspace_and_owner(client: httpx.AsyncClient) -> None:
    response = await client.post(
        "/api/v1/projects",
        json={
            "workspace_id": "00000000-0000-0000-0000-000000000001",
            "owner_user_id": "00000000-0000-0000-0000-000000000002",
            "title": "Invalid Project",
        },
    )
    assert response.status_code == 404


@pytest.mark.anyio
async def test_validation_rejects_blank_title(client: httpx.AsyncClient) -> None:
    workspace = await client.post("/api/v1/workspaces", json={"name": "Studio", "slug": "studio"})
    user = await client.post(
        "/api/v1/users", json={"email": "owner@example.com", "display_name": "Owner"}
    )

    response = await client.post(
        "/api/v1/projects",
        json={
            "workspace_id": workspace.json()["id"],
            "owner_user_id": user.json()["id"],
            "title": "   ",
        },
    )
    assert response.status_code == 422
