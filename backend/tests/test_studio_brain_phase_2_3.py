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


async def _project_context(client: httpx.AsyncClient, suffix: str = "controller") -> tuple[str, str]:
    workspace = await client.post(
        "/api/v1/workspaces",
        json={"name": f"Controller Studio {suffix}", "slug": f"controller-studio-{suffix}"},
    )
    user = await client.post(
        "/api/v1/users",
        json={
            "email": f"controller-owner-{suffix}@example.com",
            "display_name": f"Controller Owner {suffix}",
        },
    )
    project = await client.post(
        "/api/v1/projects",
        json={
            "workspace_id": workspace.json()["id"],
            "owner_user_id": user.json()["id"],
            "title": f"Controller Film {suffix}",
        },
    )
    return project.json()["id"], user.json()["id"]


async def _create_entry(
    client: httpx.AsyncClient,
    project_id: str,
    user_id: str,
    payload: dict[str, object],
) -> dict[str, object]:
    response = await client.post(
        f"/api/v1/projects/{project_id}/blackboard-entries",
        json={"author_user_id": user_id, **payload},
    )
    assert response.status_code == 201
    return response.json()


@pytest.mark.anyio
async def test_deliberation_controller_ranks_open_entries_and_records_run(
    client: httpx.AsyncClient,
) -> None:
    project_id, user_id = await _project_context(client)
    observation = await _create_entry(
        client,
        project_id,
        user_id,
        {
            "entry_type": "observation",
            "title": "Mood is consistent",
            "summary": "The visual references point in one direction.",
            "rationale": "This is useful but not blocking.",
            "confidence_level": "high",
            "severity": "low",
            "payload": {"observation": "References are restrained.", "evidence": ["ref board"]},
        },
    )
    proof_request = await _create_entry(
        client,
        project_id,
        user_id,
        {
            "entry_type": "proof_request",
            "title": "Proof before production",
            "summary": "The route is untested and production would be premature.",
            "rationale": "A cheap proof can remove a high-impact uncertainty.",
            "confidence_level": "low",
            "severity": "critical",
            "payload": {
                "proof_type": "visual_language_test",
                "question": "Can the visual system carry the thesis?",
                "acceptance_test": "Viewers describe the intended promise without narration.",
                "cheapest_useful_proof": "Three style frames and a 10 second motion sketch.",
            },
        },
    )

    run = await client.post(
        f"/api/v1/projects/{project_id}/deliberation-controller-runs",
        json={
            "created_by_user_id": user_id,
            "question": "What should the Studio Brain do next?",
        },
    )

    assert run.status_code == 201
    body = run.json()
    assert body["selected_candidate"]["blackboard_entry_id"] == proof_request["id"]
    assert body["ranked_candidates"][0]["blackboard_entry_id"] == proof_request["id"]
    assert body["ranked_candidates"][1]["blackboard_entry_id"] == observation["id"]
    assert body["deliberation_record"]["status"] == "recorded"
    assert body["deliberation_record"]["linked_entry_ids"] == [proof_request["id"]]
    assert body["deliberation_record"]["result"]["controller"] == "deterministic_v1"

    audit_events = await client.get(f"/api/v1/audit-events?project_id={project_id}")
    assert audit_events.status_code == 200
    assert ("deliberation_record", "controller_ran") in [
        (event["entity_type"], event["action"]) for event in audit_events.json()
    ]


@pytest.mark.anyio
async def test_deliberation_controller_requires_open_blackboard_entries(
    client: httpx.AsyncClient,
) -> None:
    project_id, user_id = await _project_context(client)

    run = await client.post(
        f"/api/v1/projects/{project_id}/deliberation-controller-runs",
        json={"created_by_user_id": user_id},
    )

    assert run.status_code == 422


@pytest.mark.anyio
async def test_deliberation_controller_does_not_mutate_source_of_truth(
    client: httpx.AsyncClient,
) -> None:
    project_id, user_id = await _project_context(client)
    await _create_entry(
        client,
        project_id,
        user_id,
        {
            "entry_type": "risk",
            "title": "Audience promise may be unclear",
            "summary": "The promise has not been tested.",
            "rationale": "The next action should reduce uncertainty, not approve production.",
            "confidence_level": "low",
            "severity": "high",
            "payload": {
                "risk_type": "audience_promise",
                "impact": "The film could be polished around a weak promise.",
                "mitigation": "Run a proof against audience interpretation.",
            },
        },
    )

    run = await client.post(
        f"/api/v1/projects/{project_id}/deliberation-controller-runs",
        json={"created_by_user_id": user_id},
    )
    assert run.status_code == 201

    artifacts = await client.get(f"/api/v1/projects/{project_id}/artifacts")
    decisions = await client.get(f"/api/v1/projects/{project_id}/decisions")
    creative_inputs = await client.get(f"/api/v1/projects/{project_id}/creative-inputs")
    assert artifacts.json() == []
    assert decisions.json() == []
    assert creative_inputs.json() == []
