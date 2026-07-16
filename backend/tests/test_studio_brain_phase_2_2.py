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


async def _project_context(client: httpx.AsyncClient, suffix: str = "specialist") -> tuple[str, str]:
    workspace = await client.post(
        "/api/v1/workspaces",
        json={"name": f"Specialist Studio {suffix}", "slug": f"specialist-studio-{suffix}"},
    )
    user = await client.post(
        "/api/v1/users",
        json={
            "email": f"specialist-owner-{suffix}@example.com",
            "display_name": f"Specialist Owner {suffix}",
        },
    )
    project = await client.post(
        "/api/v1/projects",
        json={
            "workspace_id": workspace.json()["id"],
            "owner_user_id": user.json()["id"],
            "title": f"Specialist Film {suffix}",
        },
    )
    return project.json()["id"], user.json()["id"]


def _proposal_payload(user_id: str) -> dict[str, object]:
    return {
        "submitted_by_user_id": user_id,
        "specialist_type": "creative_director",
        "proposal_kind": "creative_route",
        "title": "Hold treatment until proof",
        "problem_statement": "The route is plausible but not proven.",
        "recommendation": "Request a visual proof before expanding the treatment.",
        "rationale": "The next decision has high downstream cost.",
        "expected_impact": "Prevents committing production to a weak route.",
        "confidence_level": "medium",
        "severity": "high",
        "evidence": ["Audience promise is still abstract."],
        "risks": ["Delay if proof is skipped and the route fails later."],
    }


@pytest.mark.anyio
async def test_specialist_proposal_creates_linked_blackboard_entry_and_audit(
    client: httpx.AsyncClient,
) -> None:
    project_id, user_id = await _project_context(client)

    created = await client.post(
        f"/api/v1/projects/{project_id}/specialist-proposals",
        json=_proposal_payload(user_id),
    )

    assert created.status_code == 201
    proposal = created.json()
    assert proposal["specialist_type"] == "creative_director"
    assert proposal["proposal_kind"] == "creative_route"
    assert proposal["status"] == "submitted"
    assert proposal["blackboard_entry_id"]

    blackboard_entry = await client.get(
        f"/api/v1/blackboard-entries/{proposal['blackboard_entry_id']}"
    )
    assert blackboard_entry.status_code == 200
    entry = blackboard_entry.json()
    assert entry["entry_type"] == "proposal"
    assert entry["payload"]["specialist_type"] == "creative_director"
    assert entry["payload"]["recommended_action"] == proposal["recommendation"]

    listed = await client.get(
        f"/api/v1/projects/{project_id}/specialist-proposals?specialist_type=creative_director"
    )
    assert listed.status_code == 200
    assert [item["id"] for item in listed.json()] == [proposal["id"]]

    fetched = await client.get(f"/api/v1/specialist-proposals/{proposal['id']}")
    assert fetched.status_code == 200
    assert fetched.json()["blackboard_entry_id"] == proposal["blackboard_entry_id"]

    audit_events = await client.get(f"/api/v1/audit-events?project_id={project_id}")
    assert audit_events.status_code == 200
    audit_pairs = [(event["entity_type"], event["action"]) for event in audit_events.json()]
    assert ("blackboard_entry", "created") in audit_pairs
    assert ("specialist_proposal", "submitted") in audit_pairs


@pytest.mark.anyio
async def test_specialist_proposal_rejects_unsupported_specialist(
    client: httpx.AsyncClient,
) -> None:
    project_id, user_id = await _project_context(client)
    payload = _proposal_payload(user_id)
    payload["specialist_type"] = "timeline_generator"

    invalid = await client.post(
        f"/api/v1/projects/{project_id}/specialist-proposals",
        json=payload,
    )

    assert invalid.status_code == 422


@pytest.mark.anyio
async def test_specialist_proposal_target_must_belong_to_project(
    client: httpx.AsyncClient,
) -> None:
    project_a_id, user_a_id = await _project_context(client, "a")
    project_b_id, user_b_id = await _project_context(client, "b")
    artifact = await client.post(
        f"/api/v1/projects/{project_a_id}/artifacts",
        json={
            "owner_user_id": user_a_id,
            "artifact_type": "direction_bible",
            "title": "Project A Direction Bible",
        },
    )
    assert artifact.status_code == 201

    payload = _proposal_payload(user_b_id)
    payload["target_artifact_id"] = artifact.json()["id"]
    invalid = await client.post(
        f"/api/v1/projects/{project_b_id}/specialist-proposals",
        json=payload,
    )

    assert invalid.status_code == 422


@pytest.mark.anyio
async def test_specialist_proposal_does_not_mutate_source_of_truth(
    client: httpx.AsyncClient,
) -> None:
    project_id, user_id = await _project_context(client)

    created = await client.post(
        f"/api/v1/projects/{project_id}/specialist-proposals",
        json=_proposal_payload(user_id),
    )
    assert created.status_code == 201

    artifacts = await client.get(f"/api/v1/projects/{project_id}/artifacts")
    decisions = await client.get(f"/api/v1/projects/{project_id}/decisions")
    creative_inputs = await client.get(f"/api/v1/projects/{project_id}/creative-inputs")
    assert artifacts.status_code == 200
    assert decisions.status_code == 200
    assert creative_inputs.status_code == 200
    assert artifacts.json() == []
    assert decisions.json() == []
    assert creative_inputs.json() == []
