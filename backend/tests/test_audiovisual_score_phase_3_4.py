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


async def _project_context(client: httpx.AsyncClient, suffix: str = "preview") -> tuple[str, str]:
    workspace = await client.post(
        "/api/v1/workspaces",
        json={"name": f"Preview Studio {suffix}", "slug": f"preview-studio-{suffix}"},
    )
    user = await client.post(
        "/api/v1/users",
        json={
            "email": f"preview-owner-{suffix}@example.com",
            "display_name": f"Preview Owner {suffix}",
        },
    )
    project = await client.post(
        "/api/v1/projects",
        json={
            "workspace_id": workspace.json()["id"],
            "owner_user_id": user.json()["id"],
            "title": f"Preview Film {suffix}",
        },
    )
    return project.json()["id"], user.json()["id"]


async def _create_branch(client: httpx.AsyncClient, project_id: str, user_id: str) -> dict[str, object]:
    response = await client.post(
        f"/api/v1/projects/{project_id}/score-branches",
        json={
            "created_by_user_id": user_id,
            "name": "Preview score",
            "purpose": "Test whether score events work before execution.",
        },
    )
    assert response.status_code == 201
    return response.json()


async def _create_score_event(
    client: httpx.AsyncClient, branch_id: str, user_id: str
) -> dict[str, object]:
    response = await client.post(
        f"/api/v1/score-branches/{branch_id}/events",
        json={
            "created_by_user_id": user_id,
            "hierarchy_level": "beat",
            "title": "Pressure reveal",
            "sort_key": "001",
            "why": "Test whether the viewer feels pressure before explanation.",
            "what": "A withheld cue turns into a clear pressure reveal.",
            "how": "Use a card, rough board, temp narration, timing, and sound placeholder.",
            "where_when": {
                "placement": "First sequence midpoint.",
                "timing": "After the orientation beat.",
                "duration": "Elastic until screening clarifies comprehension.",
                "dependency": "Requires accepted story argument.",
            },
            "duration_policy": "elastic",
        },
    )
    assert response.status_code == 201
    return response.json()


async def _create_second_score_event(
    client: httpx.AsyncClient, branch_id: str, user_id: str
) -> dict[str, object]:
    response = await client.post(
        f"/api/v1/score-branches/{branch_id}/events",
        json={
            "created_by_user_id": user_id,
            "hierarchy_level": "beat",
            "title": "Reaction pause",
            "sort_key": "002",
            "why": "Test whether the viewer has enough time to absorb the reveal.",
            "what": "The sequence pauses on the consequence before moving forward.",
            "how": "Use a held card and restrained timing note.",
            "where_when": {
                "placement": "Immediately after the pressure reveal.",
                "timing": "Before the argument continues.",
                "duration": "Elastic until screening clarifies rhythm.",
                "dependency": "Requires the pressure reveal beat.",
            },
            "duration_policy": "elastic",
        },
    )
    assert response.status_code == 201
    return response.json()


async def _create_prototype(
    client: httpx.AsyncClient, branch_id: str, user_id: str
) -> dict[str, object]:
    response = await client.post(
        f"/api/v1/score-branches/{branch_id}/preview-prototypes",
        json={
            "created_by_user_id": user_id,
            "prototype_type": "animatic_stub",
            "title": "Pressure reveal animatic stub",
            "purpose": "Check comprehension and rhythm before execution.",
            "test_question": "Does the reveal land before any final media exists?",
        },
    )
    assert response.status_code == 201
    return response.json()


def _preview_item_payload(user_id: str, score_event_id: str, **overrides: object) -> dict[str, object]:
    payload: dict[str, object] = {
        "created_by_user_id": user_id,
        "score_event_id": score_event_id,
        "item_type": "card",
        "title": "Pressure reveal card",
        "sort_key": "001",
        "test_focus": "Whether the event's purpose is legible without final media.",
        "inspection_notes": "Reviewer should explain why the event exists and what changed.",
        "body": {
            "event_summary": "The pressure cue becomes readable.",
            "viewer_question": "What changed in the viewer's understanding?",
            "visible_information": "Only the consequence and reaction are visible.",
        },
    }
    payload.update(overrides)
    return payload


@pytest.mark.anyio
async def test_create_list_get_preview_prototype_and_item_with_audit(
    client: httpx.AsyncClient,
) -> None:
    project_id, user_id = await _project_context(client)
    branch = await _create_branch(client, project_id, user_id)
    event = await _create_score_event(client, branch["id"], user_id)
    prototype = await _create_prototype(client, branch["id"], user_id)

    created_item = await client.post(
        f"/api/v1/score-preview-prototypes/{prototype['id']}/items",
        json=_preview_item_payload(user_id, event["id"]),
    )

    assert created_item.status_code == 201
    item = created_item.json()
    assert item["prototype_id"] == prototype["id"]
    assert item["score_event_id"] == event["id"]
    assert item["score_event_why_snapshot"] == (
        "Test whether the viewer feels pressure before explanation."
    )
    assert item["body"]["viewer_question"] == "What changed in the viewer's understanding?"

    prototypes = await client.get(f"/api/v1/score-branches/{branch['id']}/preview-prototypes")
    items = await client.get(
        f"/api/v1/score-preview-prototypes/{prototype['id']}/items?item_type=card"
    )
    fetched_prototype = await client.get(f"/api/v1/score-preview-prototypes/{prototype['id']}")
    fetched_item = await client.get(f"/api/v1/score-preview-items/{item['id']}")
    assert [entry["id"] for entry in prototypes.json()] == [prototype["id"]]
    assert [entry["id"] for entry in items.json()] == [item["id"]]
    assert fetched_prototype.json()["test_question"] == (
        "Does the reveal land before any final media exists?"
    )
    assert fetched_item.json()["inspection_notes"] == (
        "Reviewer should explain why the event exists and what changed."
    )

    audit_events = await client.get(f"/api/v1/audit-events?project_id={project_id}")
    audit_pairs = [(entry["entity_type"], entry["action"]) for entry in audit_events.json()]
    assert ("audiovisual_score_preview_prototype", "created") in audit_pairs
    assert ("audiovisual_score_preview_item", "created") in audit_pairs


@pytest.mark.anyio
async def test_preview_item_requires_type_specific_body_and_inspection_focus(
    client: httpx.AsyncClient,
) -> None:
    project_id, user_id = await _project_context(client)
    branch = await _create_branch(client, project_id, user_id)
    event = await _create_score_event(client, branch["id"], user_id)
    prototype = await _create_prototype(client, branch["id"], user_id)

    missing_board_key = await client.post(
        f"/api/v1/score-preview-prototypes/{prototype['id']}/items",
        json=_preview_item_payload(
            user_id,
            event["id"],
            item_type="board",
            body={
                "composition": "Tight subject card with negative space.",
                "subject_state": "The subject understands the trap.",
            },
        ),
    )
    blank_focus = await client.post(
        f"/api/v1/score-preview-prototypes/{prototype['id']}/items",
        json=_preview_item_payload(user_id, event["id"], test_focus=" "),
    )

    assert missing_board_key.status_code == 422
    assert blank_focus.status_code == 422


@pytest.mark.anyio
async def test_preview_item_rejects_score_event_from_another_branch(
    client: httpx.AsyncClient,
) -> None:
    project_id, user_id = await _project_context(client)
    branch_a = await _create_branch(client, project_id, user_id)
    branch_b = await _create_branch(client, project_id, user_id)
    event_b = await _create_score_event(client, branch_b["id"], user_id)
    prototype_a = await _create_prototype(client, branch_a["id"], user_id)

    invalid = await client.post(
        f"/api/v1/score-preview-prototypes/{prototype_a['id']}/items",
        json=_preview_item_payload(user_id, event_b["id"]),
    )

    assert invalid.status_code == 422


@pytest.mark.anyio
async def test_preview_records_reject_cross_project_links(client: httpx.AsyncClient) -> None:
    project_a_id, user_a_id = await _project_context(client, "a")
    project_b_id, user_b_id = await _project_context(client, "b")
    branch_b = await _create_branch(client, project_b_id, user_b_id)
    event_b = await _create_score_event(client, branch_b["id"], user_b_id)
    prototype_b = await _create_prototype(client, branch_b["id"], user_b_id)
    entry_a = await client.post(
        f"/api/v1/projects/{project_a_id}/blackboard-entries",
        json={
            "author_user_id": user_a_id,
            "entry_type": "proof_request",
            "title": "External preview proof",
            "summary": "This proof request belongs to another project.",
            "rationale": "Preview records must remain project-scoped.",
            "confidence_level": "medium",
            "severity": "high",
            "payload": {
                "proof_type": "preview_screening",
                "question": "Does the prototype answer the test question?",
                "acceptance_test": "Reviewer can explain the event purpose.",
                "cheapest_useful_proof": "A card sequence screening.",
            },
        },
    )
    assert entry_a.status_code == 201

    invalid_prototype = await client.post(
        f"/api/v1/score-branches/{branch_b['id']}/preview-prototypes",
        json={
            "created_by_user_id": user_b_id,
            "prototype_type": "cards",
            "title": "Invalid linked prototype",
            "purpose": "Should reject cross-project proof links.",
            "test_question": "Will this reject the link?",
            "linked_blackboard_entry_id": entry_a.json()["id"],
        },
    )
    invalid_item = await client.post(
        f"/api/v1/score-preview-prototypes/{prototype_b['id']}/items",
        json=_preview_item_payload(
            user_b_id,
            event_b["id"],
            linked_blackboard_entry_id=entry_a.json()["id"],
        ),
    )

    assert invalid_prototype.status_code == 422
    assert invalid_item.status_code == 422


@pytest.mark.anyio
async def test_preview_foundation_does_not_create_execution_outputs(
    client: httpx.AsyncClient,
) -> None:
    project_id, user_id = await _project_context(client)
    branch = await _create_branch(client, project_id, user_id)
    event = await _create_score_event(client, branch["id"], user_id)
    prototype = await _create_prototype(client, branch["id"], user_id)

    created = await client.post(
        f"/api/v1/score-preview-prototypes/{prototype['id']}/items",
        json=_preview_item_payload(user_id, event["id"]),
    )
    assert created.status_code == 201

    artifacts = await client.get(f"/api/v1/projects/{project_id}/artifacts")
    decisions = await client.get(f"/api/v1/projects/{project_id}/decisions")
    creative_inputs = await client.get(f"/api/v1/projects/{project_id}/creative-inputs")
    assert artifacts.json() == []
    assert decisions.json() == []
    assert creative_inputs.json() == []


@pytest.mark.anyio
async def test_preview_coverage_reports_missing_and_ready_events(
    client: httpx.AsyncClient,
) -> None:
    project_id, user_id = await _project_context(client)
    branch = await _create_branch(client, project_id, user_id)
    first_event = await _create_score_event(client, branch["id"], user_id)
    second_event = await _create_second_score_event(client, branch["id"], user_id)
    prototype = await _create_prototype(client, branch["id"], user_id)

    first_item = await client.post(
        f"/api/v1/score-preview-prototypes/{prototype['id']}/items",
        json=_preview_item_payload(user_id, first_event["id"]),
    )
    assert first_item.status_code == 201

    incomplete = await client.get(f"/api/v1/score-preview-prototypes/{prototype['id']}/coverage")
    assert incomplete.status_code == 200
    incomplete_body = incomplete.json()
    assert incomplete_body["ready"] is False
    assert incomplete_body["total_score_events"] == 2
    assert incomplete_body["covered_score_events"] == 1
    assert incomplete_body["missing_score_event_ids"] == [second_event["id"]]

    second_item = await client.post(
        f"/api/v1/score-preview-prototypes/{prototype['id']}/items",
        json=_preview_item_payload(user_id, second_event["id"], sort_key="002"),
    )
    assert second_item.status_code == 201

    complete = await client.get(f"/api/v1/score-preview-prototypes/{prototype['id']}/coverage")
    complete_body = complete.json()
    assert complete_body["ready"] is True
    assert complete_body["missing_score_event_ids"] == []
    assert [event["covered"] for event in complete_body["events"]] == [True, True]
    assert complete_body["events"][0]["why"] == (
        "Test whether the viewer feels pressure before explanation."
    )
