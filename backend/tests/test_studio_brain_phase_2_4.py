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


async def _project_context(client: httpx.AsyncClient, suffix: str = "checkpoint") -> tuple[str, str]:
    workspace = await client.post(
        "/api/v1/workspaces",
        json={"name": f"Checkpoint Studio {suffix}", "slug": f"checkpoint-studio-{suffix}"},
    )
    user = await client.post(
        "/api/v1/users",
        json={
            "email": f"checkpoint-owner-{suffix}@example.com",
            "display_name": f"Checkpoint Owner {suffix}",
        },
    )
    project = await client.post(
        "/api/v1/projects",
        json={
            "workspace_id": workspace.json()["id"],
            "owner_user_id": user.json()["id"],
            "title": f"Checkpoint Film {suffix}",
        },
    )
    return project.json()["id"], user.json()["id"]


async def _create_proof_request(
    client: httpx.AsyncClient, project_id: str, user_id: str
) -> dict[str, object]:
    response = await client.post(
        f"/api/v1/projects/{project_id}/blackboard-entries",
        json={
            "author_user_id": user_id,
            "entry_type": "proof_request",
            "title": "Proof before approval",
            "summary": "The route needs human approval after proof.",
            "rationale": "Human checkpoint should link to the blocking question.",
            "confidence_level": "medium",
            "severity": "high",
            "payload": {
                "proof_type": "visual_language_test",
                "question": "Can the visual route carry the thesis?",
                "acceptance_test": "Reviewer can state the promise from the proof.",
                "cheapest_useful_proof": "Three style frames.",
            },
        },
    )
    assert response.status_code == 201
    return response.json()


@pytest.mark.anyio
async def test_create_list_get_and_decide_human_checkpoint_with_audit(
    client: httpx.AsyncClient,
) -> None:
    project_id, user_id = await _project_context(client)
    entry = await _create_proof_request(client, project_id, user_id)

    created = await client.post(
        f"/api/v1/projects/{project_id}/human-checkpoints",
        json={
            "requested_by_user_id": user_id,
            "checkpoint_type": "visual_language",
            "title": "Approve visual language route",
            "summary": "Human approval is required before production planning.",
            "linked_blackboard_entry_id": entry["id"],
        },
    )

    assert created.status_code == 201
    checkpoint = created.json()
    assert checkpoint["decision_status"] == "pending"
    assert checkpoint["linked_blackboard_entry_id"] == entry["id"]

    listed = await client.get(
        f"/api/v1/projects/{project_id}/human-checkpoints"
        "?checkpoint_type=visual_language&decision_status=pending"
    )
    assert listed.status_code == 200
    assert [item["id"] for item in listed.json()] == [checkpoint["id"]]

    fetched = await client.get(f"/api/v1/human-checkpoints/{checkpoint['id']}")
    assert fetched.status_code == 200
    assert fetched.json()["checkpoint_type"] == "visual_language"

    decided = await client.patch(
        f"/api/v1/human-checkpoints/{checkpoint['id']}/decision",
        json={
            "decided_by_user_id": user_id,
            "decision_status": "approved",
            "decision_rationale": "The proof is sufficient for this stage.",
        },
    )
    assert decided.status_code == 200
    assert decided.json()["decision_status"] == "approved"
    assert decided.json()["decision_rationale"] == "The proof is sufficient for this stage."

    audit_events = await client.get(f"/api/v1/audit-events?project_id={project_id}")
    assert audit_events.status_code == 200
    audit_pairs = [(event["entity_type"], event["action"]) for event in audit_events.json()]
    assert ("human_checkpoint", "created") in audit_pairs
    assert ("human_checkpoint", "decided") in audit_pairs


@pytest.mark.anyio
async def test_human_checkpoint_decision_requires_rationale(client: httpx.AsyncClient) -> None:
    project_id, user_id = await _project_context(client)
    created = await client.post(
        f"/api/v1/projects/{project_id}/human-checkpoints",
        json={
            "requested_by_user_id": user_id,
            "checkpoint_type": "project_thesis",
            "title": "Approve thesis",
            "summary": "The project thesis needs an accountable approval.",
        },
    )
    assert created.status_code == 201

    invalid = await client.patch(
        f"/api/v1/human-checkpoints/{created.json()['id']}/decision",
        json={
            "decided_by_user_id": user_id,
            "decision_status": "approved",
            "decision_rationale": " ",
        },
    )

    assert invalid.status_code == 422


@pytest.mark.anyio
async def test_human_checkpoint_rejects_cross_project_links(client: httpx.AsyncClient) -> None:
    project_a_id, user_a_id = await _project_context(client, "a")
    project_b_id, user_b_id = await _project_context(client, "b")
    entry = await _create_proof_request(client, project_a_id, user_a_id)

    invalid = await client.post(
        f"/api/v1/projects/{project_b_id}/human-checkpoints",
        json={
            "requested_by_user_id": user_b_id,
            "checkpoint_type": "creative_route",
            "title": "Cross-project approval",
            "summary": "This should not link to another project.",
            "linked_blackboard_entry_id": entry["id"],
        },
    )

    assert invalid.status_code == 422


@pytest.mark.anyio
async def test_human_checkpoint_does_not_mutate_source_of_truth(
    client: httpx.AsyncClient,
) -> None:
    project_id, user_id = await _project_context(client)
    created = await client.post(
        f"/api/v1/projects/{project_id}/human-checkpoints",
        json={
            "requested_by_user_id": user_id,
            "checkpoint_type": "final_release",
            "title": "Final release approval",
            "summary": "Release must be human approved, but this record does not publish.",
        },
    )
    assert created.status_code == 201
    decided = await client.patch(
        f"/api/v1/human-checkpoints/{created.json()['id']}/decision",
        json={
            "decided_by_user_id": user_id,
            "decision_status": "blocked",
            "decision_rationale": "Rights evidence is missing.",
        },
    )
    assert decided.status_code == 200

    artifacts = await client.get(f"/api/v1/projects/{project_id}/artifacts")
    decisions = await client.get(f"/api/v1/projects/{project_id}/decisions")
    creative_inputs = await client.get(f"/api/v1/projects/{project_id}/creative-inputs")
    assert artifacts.json() == []
    assert decisions.json() == []
    assert creative_inputs.json() == []
