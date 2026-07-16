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


async def _project_context(client: httpx.AsyncClient, suffix: str = "score") -> tuple[str, str]:
    workspace = await client.post(
        "/api/v1/workspaces",
        json={"name": f"Score Studio {suffix}", "slug": f"score-studio-{suffix}"},
    )
    user = await client.post(
        "/api/v1/users",
        json={
            "email": f"score-owner-{suffix}@example.com",
            "display_name": f"Score Owner {suffix}",
        },
    )
    project = await client.post(
        "/api/v1/projects",
        json={
            "workspace_id": workspace.json()["id"],
            "owner_user_id": user.json()["id"],
            "title": f"Score Film {suffix}",
        },
    )
    return project.json()["id"], user.json()["id"]


def _event_payload(user_id: str, **overrides: object) -> dict[str, object]:
    payload: dict[str, object] = {
        "created_by_user_id": user_id,
        "hierarchy_level": "scene",
        "title": "Audience promise turn",
        "sort_key": "001.001",
        "why": "Shift the viewer from curiosity into concern.",
        "what": "The protagonist recognizes the cost of the route.",
        "how": "Hold on constrained movement, then introduce restrained low-frequency sound.",
        "where_when": {
            "placement": "Opening movement, after the premise is established.",
            "timing": "Relative to the first proof beat.",
            "duration": "Elastic, roughly one short scene.",
            "dependency": "Requires accepted creative route and visual language proof.",
        },
        "duration_policy": "elastic",
    }
    payload.update(overrides)
    return payload


async def _create_branch(client: httpx.AsyncClient, project_id: str, user_id: str) -> dict[str, object]:
    response = await client.post(
        f"/api/v1/projects/{project_id}/score-branches",
        json={
            "created_by_user_id": user_id,
            "name": "Primary editorial score",
            "purpose": "Capture the intended viewer experience before timeline execution.",
        },
    )
    assert response.status_code == 201
    return response.json()


@pytest.mark.anyio
async def test_create_list_get_score_branch_and_event_with_audit(
    client: httpx.AsyncClient,
) -> None:
    project_id, user_id = await _project_context(client)
    branch = await _create_branch(client, project_id, user_id)

    created = await client.post(
        f"/api/v1/score-branches/{branch['id']}/events",
        json=_event_payload(user_id),
    )

    assert created.status_code == 201
    event = created.json()
    assert event["project_id"] == project_id
    assert event["why"] == "Shift the viewer from curiosity into concern."
    assert event["what"] == "The protagonist recognizes the cost of the route."
    assert event["how"].startswith("Hold on constrained movement")
    assert event["where_when"]["dependency"] == (
        "Requires accepted creative route and visual language proof."
    )

    listed_branches = await client.get(f"/api/v1/projects/{project_id}/score-branches")
    assert listed_branches.status_code == 200
    assert [item["id"] for item in listed_branches.json()] == [branch["id"]]

    listed_events = await client.get(f"/api/v1/score-branches/{branch['id']}/events")
    assert listed_events.status_code == 200
    assert [item["id"] for item in listed_events.json()] == [event["id"]]

    fetched_event = await client.get(f"/api/v1/score-events/{event['id']}")
    assert fetched_event.status_code == 200
    assert fetched_event.json()["title"] == "Audience promise turn"

    audit_events = await client.get(f"/api/v1/audit-events?project_id={project_id}")
    assert audit_events.status_code == 200
    audit_pairs = [(item["entity_type"], item["action"]) for item in audit_events.json()]
    assert ("audiovisual_score_branch", "created") in audit_pairs
    assert ("audiovisual_score_event", "created") in audit_pairs


@pytest.mark.anyio
async def test_score_event_requires_why_what_how_and_where_when(
    client: httpx.AsyncClient,
) -> None:
    project_id, user_id = await _project_context(client)
    branch = await _create_branch(client, project_id, user_id)

    missing_why = await client.post(
        f"/api/v1/score-branches/{branch['id']}/events",
        json=_event_payload(user_id, why=" "),
    )
    missing_dependency = await client.post(
        f"/api/v1/score-branches/{branch['id']}/events",
        json=_event_payload(
            user_id,
            where_when={
                "placement": "Opening movement.",
                "timing": "After the premise.",
                "duration": "Elastic.",
                "dependency": " ",
            },
        ),
    )

    assert missing_why.status_code == 422
    assert missing_dependency.status_code == 422


@pytest.mark.anyio
async def test_script_input_does_not_create_score_automatically(
    client: httpx.AsyncClient,
) -> None:
    project_id, user_id = await _project_context(client)

    created_input = await client.post(
        f"/api/v1/projects/{project_id}/creative-inputs",
        json={
            "submitted_by_user_id": user_id,
            "input_type": "script",
            "title": "Draft script",
            "body": {"text": "INT. ROOM - A line that must not become timeline truth."},
        },
    )
    assert created_input.status_code == 201

    branches = await client.get(f"/api/v1/projects/{project_id}/score-branches")
    artifacts = await client.get(f"/api/v1/projects/{project_id}/artifacts")
    decisions = await client.get(f"/api/v1/projects/{project_id}/decisions")
    assert branches.status_code == 200
    assert branches.json() == []
    assert artifacts.json() == []
    assert decisions.json() == []


@pytest.mark.anyio
async def test_score_event_rejects_cross_project_blackboard_link(
    client: httpx.AsyncClient,
) -> None:
    project_a_id, user_a_id = await _project_context(client, "a")
    project_b_id, user_b_id = await _project_context(client, "b")
    branch_b = await _create_branch(client, project_b_id, user_b_id)
    entry = await client.post(
        f"/api/v1/projects/{project_a_id}/blackboard-entries",
        json={
            "author_user_id": user_a_id,
            "entry_type": "proof_request",
            "title": "Proof from project A",
            "summary": "This proof request belongs to another project.",
            "rationale": "Score events must not cross project boundaries.",
            "confidence_level": "medium",
            "severity": "high",
            "payload": {
                "proof_type": "score_intent",
                "question": "Does the beat carry the intended shift?",
                "acceptance_test": "Reviewer can name the intended viewer response.",
                "cheapest_useful_proof": "A one-page beat proof.",
            },
        },
    )
    assert entry.status_code == 201

    invalid = await client.post(
        f"/api/v1/score-branches/{branch_b['id']}/events",
        json=_event_payload(user_b_id, linked_blackboard_entry_id=entry.json()["id"]),
    )

    assert invalid.status_code == 422


@pytest.mark.anyio
async def test_parent_event_must_belong_to_same_branch(client: httpx.AsyncClient) -> None:
    project_id, user_id = await _project_context(client)
    branch_a = await _create_branch(client, project_id, user_id)
    branch_b = await _create_branch(client, project_id, user_id)
    parent = await client.post(
        f"/api/v1/score-branches/{branch_a['id']}/events",
        json=_event_payload(user_id, title="Parent event", sort_key="001"),
    )
    assert parent.status_code == 201

    invalid = await client.post(
        f"/api/v1/score-branches/{branch_b['id']}/events",
        json=_event_payload(user_id, parent_event_id=parent.json()["id"], sort_key="002"),
    )

    assert invalid.status_code == 422
