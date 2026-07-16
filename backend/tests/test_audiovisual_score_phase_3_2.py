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


async def _project_context(client: httpx.AsyncClient, suffix: str = "lanes") -> tuple[str, str]:
    workspace = await client.post(
        "/api/v1/workspaces",
        json={"name": f"Lane Studio {suffix}", "slug": f"lane-studio-{suffix}"},
    )
    user = await client.post(
        "/api/v1/users",
        json={
            "email": f"lane-owner-{suffix}@example.com",
            "display_name": f"Lane Owner {suffix}",
        },
    )
    project = await client.post(
        "/api/v1/projects",
        json={
            "workspace_id": workspace.json()["id"],
            "owner_user_id": user.json()["id"],
            "title": f"Lane Film {suffix}",
        },
    )
    return project.json()["id"], user.json()["id"]


async def _create_score_event(
    client: httpx.AsyncClient, project_id: str, user_id: str
) -> tuple[dict[str, object], dict[str, object]]:
    branch = await client.post(
        f"/api/v1/projects/{project_id}/score-branches",
        json={
            "created_by_user_id": user_id,
            "name": "Lane score",
            "purpose": "Coordinate craft lanes above timeline execution.",
        },
    )
    assert branch.status_code == 201
    event = await client.post(
        f"/api/v1/score-branches/{branch.json()['id']}/events",
        json={
            "created_by_user_id": user_id,
            "hierarchy_level": "scene",
            "title": "Recognition beat",
            "sort_key": "001",
            "why": "Make the viewer understand the cost before the reveal.",
            "what": "The subject recognizes the central consequence.",
            "how": "Use a restrained image, held rhythm, and sound pressure.",
            "where_when": {
                "placement": "Opening sequence.",
                "timing": "After the thesis setup.",
                "duration": "Elastic short beat.",
                "dependency": "Needs accepted story argument.",
            },
            "duration_policy": "elastic",
        },
    )
    assert event.status_code == 201
    return branch.json(), event.json()


def _lane_payload(user_id: str, **overrides: object) -> dict[str, object]:
    payload: dict[str, object] = {
        "created_by_user_id": user_id,
        "lane_type": "audience_state",
        "title": "Audience uncertainty turn",
        "intent": "Move audience from oriented curiosity into productive uncertainty.",
        "content": {
            "entry_state": "Curious and oriented.",
            "exit_state": "Concerned about the cost.",
            "attention_target": "The subject's realization.",
        },
    }
    payload.update(overrides)
    return payload


@pytest.mark.anyio
async def test_create_list_get_score_lane_entry_with_audit(client: httpx.AsyncClient) -> None:
    project_id, user_id = await _project_context(client)
    branch, event = await _create_score_event(client, project_id, user_id)

    created = await client.post(
        f"/api/v1/score-events/{event['id']}/lane-entries",
        json=_lane_payload(user_id),
    )

    assert created.status_code == 201
    lane_entry = created.json()
    assert lane_entry["branch_id"] == branch["id"]
    assert lane_entry["score_event_id"] == event["id"]
    assert lane_entry["lane_type"] == "audience_state"
    assert lane_entry["content"]["attention_target"] == "The subject's realization."

    event_entries = await client.get(
        f"/api/v1/score-events/{event['id']}/lane-entries?lane_type=audience_state"
    )
    assert event_entries.status_code == 200
    assert [item["id"] for item in event_entries.json()] == [lane_entry["id"]]

    branch_entries = await client.get(
        f"/api/v1/score-branches/{branch['id']}/lane-entries?lane_type=audience_state"
    )
    assert branch_entries.status_code == 200
    assert [item["id"] for item in branch_entries.json()] == [lane_entry["id"]]

    fetched = await client.get(f"/api/v1/score-lane-entries/{lane_entry['id']}")
    assert fetched.status_code == 200
    assert fetched.json()["intent"] == (
        "Move audience from oriented curiosity into productive uncertainty."
    )

    audit_events = await client.get(f"/api/v1/audit-events?project_id={project_id}")
    assert audit_events.status_code == 200
    audit_pairs = [(item["entity_type"], item["action"]) for item in audit_events.json()]
    assert ("audiovisual_score_lane_entry", "created") in audit_pairs


@pytest.mark.anyio
async def test_score_lane_entry_requires_lane_specific_content(
    client: httpx.AsyncClient,
) -> None:
    project_id, user_id = await _project_context(client)
    _, event = await _create_score_event(client, project_id, user_id)

    missing_required_key = await client.post(
        f"/api/v1/score-events/{event['id']}/lane-entries",
        json=_lane_payload(
            user_id,
            lane_type="sound_music",
            content={
                "sound_source": "Room tone and restrained pressure.",
                "dynamic_state": "Low and narrowing.",
            },
        ),
    )
    blank_intent = await client.post(
        f"/api/v1/score-events/{event['id']}/lane-entries",
        json=_lane_payload(user_id, intent=" "),
    )

    assert missing_required_key.status_code == 422
    assert blank_intent.status_code == 422


@pytest.mark.anyio
async def test_score_lane_entry_rejects_cross_project_links(
    client: httpx.AsyncClient,
) -> None:
    project_a_id, user_a_id = await _project_context(client, "a")
    project_b_id, user_b_id = await _project_context(client, "b")
    _, event_b = await _create_score_event(client, project_b_id, user_b_id)
    entry_a = await client.post(
        f"/api/v1/projects/{project_a_id}/blackboard-entries",
        json={
            "author_user_id": user_a_id,
            "entry_type": "proof_request",
            "title": "External proof request",
            "summary": "This belongs to another project.",
            "rationale": "Lane links must remain project-scoped.",
            "confidence_level": "medium",
            "severity": "high",
            "payload": {
                "proof_type": "lane_content",
                "question": "Is the sound intent proven?",
                "acceptance_test": "Reviewer can identify the sound pressure shift.",
                "cheapest_useful_proof": "A short sound sketch.",
            },
        },
    )
    assert entry_a.status_code == 201

    invalid = await client.post(
        f"/api/v1/score-events/{event_b['id']}/lane-entries",
        json=_lane_payload(user_b_id, linked_blackboard_entry_id=entry_a.json()["id"]),
    )

    assert invalid.status_code == 422


@pytest.mark.anyio
async def test_score_lane_entry_does_not_mutate_source_of_truth(
    client: httpx.AsyncClient,
) -> None:
    project_id, user_id = await _project_context(client)
    _, event = await _create_score_event(client, project_id, user_id)

    created = await client.post(
        f"/api/v1/score-events/{event['id']}/lane-entries",
        json=_lane_payload(user_id),
    )
    assert created.status_code == 201

    artifacts = await client.get(f"/api/v1/projects/{project_id}/artifacts")
    decisions = await client.get(f"/api/v1/projects/{project_id}/decisions")
    creative_inputs = await client.get(f"/api/v1/projects/{project_id}/creative-inputs")
    assert artifacts.json() == []
    assert decisions.json() == []
    assert creative_inputs.json() == []
