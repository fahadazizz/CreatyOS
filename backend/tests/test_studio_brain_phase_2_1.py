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


async def _project_context(client: httpx.AsyncClient, suffix: str = "brain") -> tuple[str, str]:
    workspace = await client.post(
        "/api/v1/workspaces",
        json={"name": f"Studio Brain {suffix}", "slug": f"studio-brain-{suffix}"},
    )
    user = await client.post(
        "/api/v1/users",
        json={
            "email": f"brain-owner-{suffix}@example.com",
            "display_name": f"Brain Owner {suffix}",
        },
    )
    project = await client.post(
        "/api/v1/projects",
        json={
            "workspace_id": workspace.json()["id"],
            "owner_user_id": user.json()["id"],
            "title": f"Brain Film {suffix}",
        },
    )
    return project.json()["id"], user.json()["id"]


def _proof_request_payload() -> dict[str, str]:
    return {
        "proof_type": "visual_language_test",
        "question": "Can restrained product motion carry the thesis?",
        "acceptance_test": "Reviewers can state the intended product feeling without narration.",
        "cheapest_useful_proof": "Three still frames plus a 10 second motion sketch.",
    }


@pytest.mark.anyio
async def test_create_list_filter_blackboard_entry_and_audit(
    client: httpx.AsyncClient,
) -> None:
    project_id, user_id = await _project_context(client)

    created = await client.post(
        f"/api/v1/projects/{project_id}/blackboard-entries",
        json={
            "author_user_id": user_id,
            "entry_type": "proof_request",
            "title": "Need visual proof before production",
            "summary": "The visual language is still an assumption.",
            "rationale": "A production plan would be premature without checking the route.",
            "confidence_level": "medium",
            "severity": "high",
            "payload": _proof_request_payload(),
        },
    )

    assert created.status_code == 201
    entry = created.json()
    assert entry["entry_type"] == "proof_request"
    assert entry["status"] == "open"
    assert entry["payload"]["cheapest_useful_proof"].startswith("Three still")

    listed = await client.get(
        f"/api/v1/projects/{project_id}/blackboard-entries?entry_type=proof_request&status=open"
    )
    assert listed.status_code == 200
    assert [item["id"] for item in listed.json()] == [entry["id"]]

    fetched = await client.get(f"/api/v1/blackboard-entries/{entry['id']}")
    assert fetched.status_code == 200
    assert fetched.json()["title"] == "Need visual proof before production"

    audit_events = await client.get(f"/api/v1/audit-events?project_id={project_id}")
    assert audit_events.status_code == 200
    assert ("blackboard_entry", "created") in [
        (event["entity_type"], event["action"]) for event in audit_events.json()
    ]


@pytest.mark.anyio
async def test_blackboard_entry_requires_type_specific_payload(
    client: httpx.AsyncClient,
) -> None:
    project_id, user_id = await _project_context(client)

    invalid = await client.post(
        f"/api/v1/projects/{project_id}/blackboard-entries",
        json={
            "author_user_id": user_id,
            "entry_type": "proof_request",
            "title": "Vague proof request",
            "summary": "Missing the required proof structure.",
            "rationale": "This should not become chat-like memory.",
            "confidence_level": "low",
            "severity": "medium",
            "payload": {"question": "Is this enough?"},
        },
    )

    assert invalid.status_code == 422


@pytest.mark.anyio
async def test_blackboard_entry_target_must_belong_to_project(
    client: httpx.AsyncClient,
) -> None:
    project_a_id, user_a_id = await _project_context(client, "a")
    project_b_id, user_b_id = await _project_context(client, "b")

    artifact = await client.post(
        f"/api/v1/projects/{project_a_id}/artifacts",
        json={
            "owner_user_id": user_a_id,
            "artifact_type": "visual_language",
            "title": "Project A Visual Language",
        },
    )
    assert artifact.status_code == 201

    invalid = await client.post(
        f"/api/v1/projects/{project_b_id}/blackboard-entries",
        json={
            "author_user_id": user_b_id,
            "entry_type": "observation",
            "title": "Cross-project observation",
            "summary": "This tries to attach to another project artifact.",
            "rationale": "Targets must preserve project boundaries.",
            "confidence_level": "high",
            "severity": "low",
            "payload": {"observation": "Useful language", "evidence": ["frame ref"]},
            "target_artifact_id": artifact.json()["id"],
        },
    )

    assert invalid.status_code == 422


@pytest.mark.anyio
async def test_blackboard_status_update_writes_audit(client: httpx.AsyncClient) -> None:
    project_id, user_id = await _project_context(client)
    created = await client.post(
        f"/api/v1/projects/{project_id}/blackboard-entries",
        json={
            "author_user_id": user_id,
            "entry_type": "risk",
            "title": "Route may not survive edit",
            "summary": "The edit direction could flatten the promise.",
            "rationale": "The risk needs explicit handling before production.",
            "confidence_level": "medium",
            "severity": "critical",
            "payload": {
                "risk_type": "creative_route",
                "impact": "Premature production on a weak route.",
                "mitigation": "Run a proof and capture viewer interpretation.",
            },
        },
    )
    assert created.status_code == 201

    updated = await client.patch(
        f"/api/v1/blackboard-entries/{created.json()['id']}/status",
        json={"status": "resolved"},
    )

    assert updated.status_code == 200
    assert updated.json()["status"] == "resolved"

    audit_events = await client.get(f"/api/v1/audit-events?project_id={project_id}")
    assert audit_events.status_code == 200
    assert ("blackboard_entry", "status_changed") in [
        (event["entity_type"], event["action"]) for event in audit_events.json()
    ]


@pytest.mark.anyio
async def test_deliberation_record_links_entries_without_mutating_source_of_truth(
    client: httpx.AsyncClient,
) -> None:
    project_id, user_id = await _project_context(client)
    proposal = await client.post(
        f"/api/v1/projects/{project_id}/blackboard-entries",
        json={
            "author_user_id": user_id,
            "entry_type": "proposal",
            "title": "Test before expanding treatment",
            "summary": "A proof should precede more writing.",
            "rationale": "The uncertain point is high impact and reversible.",
            "confidence_level": "medium",
            "severity": "high",
            "payload": {
                "proposal_type": "next_action",
                "recommended_action": "Create a visual proof request.",
                "expected_impact": "Avoids committing production to an untested route.",
            },
        },
    )
    proof_request = await client.post(
        f"/api/v1/projects/{project_id}/blackboard-entries",
        json={
            "author_user_id": user_id,
            "entry_type": "proof_request",
            "title": "Proof route before source-of-truth change",
            "summary": "Resolve the highest uncertainty first.",
            "rationale": "Deliberation records should route the next proof, not mutate artifacts.",
            "confidence_level": "high",
            "severity": "high",
            "payload": _proof_request_payload(),
        },
    )
    assert proposal.status_code == 201
    assert proof_request.status_code == 201

    deliberation = await client.post(
        f"/api/v1/projects/{project_id}/deliberations",
        json={
            "created_by_user_id": user_id,
            "phase": "decide",
            "question": "What is the cheapest useful next proof?",
            "priority_inputs": {
                "creative_impact": 5,
                "uncertainty": 4,
                "irreversibility": 4,
                "cost_of_delay": 3,
                "proof_cost": 2,
                "dependency_blockage": 5,
            },
            "linked_entry_ids": [proposal.json()["id"], proof_request.json()["id"]],
            "recommended_next_action": "Run the visual language proof before accepting treatment changes.",
            "rationale": "The route has high downstream impact and a low-cost proof exists.",
            "result": {"decision": "request_proof"},
        },
    )

    assert deliberation.status_code == 201
    record = deliberation.json()
    assert record["phase"] == "decide"
    assert record["linked_entry_ids"] == [proposal.json()["id"], proof_request.json()["id"]]
    assert record["priority_inputs"]["creative_impact"] == 5

    artifacts = await client.get(f"/api/v1/projects/{project_id}/artifacts")
    decisions = await client.get(f"/api/v1/projects/{project_id}/decisions")
    assert artifacts.status_code == 200
    assert decisions.status_code == 200
    assert artifacts.json() == []
    assert decisions.json() == []

    audit_events = await client.get(f"/api/v1/audit-events?project_id={project_id}")
    assert ("deliberation_record", "created") in [
        (event["entity_type"], event["action"]) for event in audit_events.json()
    ]


@pytest.mark.anyio
async def test_deliberation_rejects_cross_project_blackboard_links(
    client: httpx.AsyncClient,
) -> None:
    project_a_id, user_a_id = await _project_context(client, "a")
    project_b_id, user_b_id = await _project_context(client, "b")
    entry = await client.post(
        f"/api/v1/projects/{project_a_id}/blackboard-entries",
        json={
            "author_user_id": user_a_id,
            "entry_type": "missing_information",
            "title": "Audience evidence missing",
            "summary": "The audience promise has no evidence yet.",
            "rationale": "A different project must not deliberate over this entry.",
            "confidence_level": "high",
            "severity": "high",
            "payload": {
                "question": "What audience problem is actually being solved?",
                "needed_for": "Project thesis approval",
            },
        },
    )
    assert entry.status_code == 201

    invalid = await client.post(
        f"/api/v1/projects/{project_b_id}/deliberations",
        json={
            "created_by_user_id": user_b_id,
            "phase": "frame",
            "question": "Can another project use this entry?",
            "priority_inputs": {
                "creative_impact": 3,
                "uncertainty": 3,
                "irreversibility": 3,
                "cost_of_delay": 3,
                "proof_cost": 3,
                "dependency_blockage": 3,
            },
            "linked_entry_ids": [entry.json()["id"]],
            "recommended_next_action": "Reject cross-project link.",
            "rationale": "Blackboard memory is project-scoped.",
        },
    )

    assert invalid.status_code == 422
