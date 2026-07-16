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


async def _project_context(
    client: httpx.AsyncClient, suffix: str = "relationships"
) -> tuple[str, str]:
    workspace = await client.post(
        "/api/v1/workspaces",
        json={"name": f"Cut Studio {suffix}", "slug": f"cut-studio-{suffix}"},
    )
    user = await client.post(
        "/api/v1/users",
        json={
            "email": f"cut-owner-{suffix}@example.com",
            "display_name": f"Cut Owner {suffix}",
        },
    )
    project = await client.post(
        "/api/v1/projects",
        json={
            "workspace_id": workspace.json()["id"],
            "owner_user_id": user.json()["id"],
            "title": f"Cut Film {suffix}",
        },
    )
    return project.json()["id"], user.json()["id"]


async def _create_branch(client: httpx.AsyncClient, project_id: str, user_id: str) -> dict[str, object]:
    response = await client.post(
        f"/api/v1/projects/{project_id}/score-branches",
        json={
            "created_by_user_id": user_id,
            "name": "Cut logic score",
            "purpose": "Represent editorial relationships before timeline execution.",
        },
    )
    assert response.status_code == 201
    return response.json()


async def _create_score_event(
    client: httpx.AsyncClient,
    branch_id: str,
    user_id: str,
    *,
    title: str,
    sort_key: str,
) -> dict[str, object]:
    response = await client.post(
        f"/api/v1/score-branches/{branch_id}/events",
        json={
            "created_by_user_id": user_id,
            "hierarchy_level": "beat",
            "title": title,
            "sort_key": sort_key,
            "why": "Shape the viewer's understanding of the argument.",
            "what": f"{title} changes the viewer's information state.",
            "how": "Use authored image, sound, rhythm, and withheld information.",
            "where_when": {
                "placement": "Inside the first sequence.",
                "timing": "Relative to the prior beat.",
                "duration": "Elastic beat duration.",
                "dependency": "Requires the sequence thesis.",
            },
            "duration_policy": "elastic",
        },
    )
    assert response.status_code == 201
    return response.json()


async def _create_event_pair(
    client: httpx.AsyncClient, project_id: str, user_id: str
) -> tuple[dict[str, object], dict[str, object], dict[str, object]]:
    branch = await _create_branch(client, project_id, user_id)
    first = await _create_score_event(
        client, branch["id"], user_id, title="Setup beat", sort_key="001"
    )
    second = await _create_score_event(
        client, branch["id"], user_id, title="Reveal beat", sort_key="002"
    )
    return branch, first, second


def _relationship_payload(user_id: str, to_event_id: str, **overrides: object) -> dict[str, object]:
    payload: dict[str, object] = {
        "created_by_user_id": user_id,
        "to_event_id": to_event_id,
        "relationship_type": "reveal",
        "title": "Setup pays into reveal",
        "rationale": "The first beat withholds cause so the second beat can reveal motive.",
        "expected_viewer_effect": "Viewer reinterprets the prior beat with new concern.",
        "timing_logic": "Cut only after the setup beat lands as a question.",
        "continuity_impact": "Preserve attention target while changing information state.",
    }
    payload.update(overrides)
    return payload


@pytest.mark.anyio
async def test_create_list_get_score_event_relationship_with_audit(
    client: httpx.AsyncClient,
) -> None:
    project_id, user_id = await _project_context(client)
    branch, first, second = await _create_event_pair(client, project_id, user_id)

    created = await client.post(
        f"/api/v1/score-events/{first['id']}/relationships",
        json=_relationship_payload(user_id, second["id"]),
    )

    assert created.status_code == 201
    relationship = created.json()
    assert relationship["branch_id"] == branch["id"]
    assert relationship["from_event_id"] == first["id"]
    assert relationship["to_event_id"] == second["id"]
    assert relationship["relationship_type"] == "reveal"
    assert relationship["expected_viewer_effect"] == (
        "Viewer reinterprets the prior beat with new concern."
    )

    outgoing = await client.get(
        f"/api/v1/score-events/{first['id']}/relationships?direction=outgoing"
    )
    incoming = await client.get(
        f"/api/v1/score-events/{second['id']}/relationships?direction=incoming"
    )
    branch_relationships = await client.get(
        f"/api/v1/score-branches/{branch['id']}/relationships?relationship_type=reveal"
    )
    fetched = await client.get(f"/api/v1/score-relationships/{relationship['id']}")
    assert [item["id"] for item in outgoing.json()] == [relationship["id"]]
    assert [item["id"] for item in incoming.json()] == [relationship["id"]]
    assert [item["id"] for item in branch_relationships.json()] == [relationship["id"]]
    assert fetched.json()["timing_logic"] == "Cut only after the setup beat lands as a question."

    audit_events = await client.get(f"/api/v1/audit-events?project_id={project_id}")
    audit_pairs = [(item["entity_type"], item["action"]) for item in audit_events.json()]
    assert ("audiovisual_score_event_relationship", "created") in audit_pairs


@pytest.mark.anyio
async def test_score_event_relationship_requires_editorial_reasoning_fields(
    client: httpx.AsyncClient,
) -> None:
    project_id, user_id = await _project_context(client)
    _, first, second = await _create_event_pair(client, project_id, user_id)

    blank_rationale = await client.post(
        f"/api/v1/score-events/{first['id']}/relationships",
        json=_relationship_payload(user_id, second["id"], rationale=" "),
    )
    missing_viewer_effect = await client.post(
        f"/api/v1/score-events/{first['id']}/relationships",
        json={
            "created_by_user_id": user_id,
            "to_event_id": second["id"],
            "relationship_type": "contrast",
            "title": "Missing viewer effect",
            "rationale": "Contrast changes the argument.",
            "timing_logic": "Place after the calm beat.",
            "continuity_impact": "Break rhythm intentionally.",
        },
    )

    assert blank_rationale.status_code == 422
    assert missing_viewer_effect.status_code == 422


@pytest.mark.anyio
async def test_score_event_relationship_rejects_self_and_cross_branch(
    client: httpx.AsyncClient,
) -> None:
    project_id, user_id = await _project_context(client)
    _, first, second = await _create_event_pair(client, project_id, user_id)
    other_branch = await _create_branch(client, project_id, user_id)
    other_event = await _create_score_event(
        client, other_branch["id"], user_id, title="Other branch beat", sort_key="001"
    )

    self_link = await client.post(
        f"/api/v1/score-events/{first['id']}/relationships",
        json=_relationship_payload(user_id, first["id"]),
    )
    cross_branch = await client.post(
        f"/api/v1/score-events/{second['id']}/relationships",
        json=_relationship_payload(user_id, other_event["id"]),
    )

    assert self_link.status_code == 422
    assert cross_branch.status_code == 422


@pytest.mark.anyio
async def test_score_event_relationship_rejects_cross_project_links(
    client: httpx.AsyncClient,
) -> None:
    project_a_id, user_a_id = await _project_context(client, "a")
    project_b_id, user_b_id = await _project_context(client, "b")
    _, first_b, second_b = await _create_event_pair(client, project_b_id, user_b_id)
    entry_a = await client.post(
        f"/api/v1/projects/{project_a_id}/blackboard-entries",
        json={
            "author_user_id": user_a_id,
            "entry_type": "proof_request",
            "title": "External relationship proof",
            "summary": "This proof request belongs to another project.",
            "rationale": "Relationship links must remain project-scoped.",
            "confidence_level": "medium",
            "severity": "high",
            "payload": {
                "proof_type": "cut_logic",
                "question": "Does the reveal relationship work?",
                "acceptance_test": "Reviewer can explain why the reveal lands.",
                "cheapest_useful_proof": "A board pair with notes.",
            },
        },
    )
    assert entry_a.status_code == 201

    invalid = await client.post(
        f"/api/v1/score-events/{first_b['id']}/relationships",
        json=_relationship_payload(
            user_b_id,
            second_b["id"],
            linked_blackboard_entry_id=entry_a.json()["id"],
        ),
    )

    assert invalid.status_code == 422


@pytest.mark.anyio
async def test_score_event_relationship_does_not_mutate_source_of_truth(
    client: httpx.AsyncClient,
) -> None:
    project_id, user_id = await _project_context(client)
    _, first, second = await _create_event_pair(client, project_id, user_id)

    created = await client.post(
        f"/api/v1/score-events/{first['id']}/relationships",
        json=_relationship_payload(user_id, second["id"]),
    )
    assert created.status_code == 201

    artifacts = await client.get(f"/api/v1/projects/{project_id}/artifacts")
    decisions = await client.get(f"/api/v1/projects/{project_id}/decisions")
    creative_inputs = await client.get(f"/api/v1/projects/{project_id}/creative-inputs")
    assert artifacts.json() == []
    assert decisions.json() == []
    assert creative_inputs.json() == []
