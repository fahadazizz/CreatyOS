# Runbook

## Milestone 0

Milestone 0 is documentation-only.

To review Milestone 0:

1. Read `AGENTS.md`.
2. Read `docs/creative_director_os_build_plan.md`.
3. Read `docs/creative_director_os_reference_architecture.md`.
4. Read `docs/milestones/milestone_0.md`.
5. Read `docs/specs/product_doctrine_and_anti_slop.md`.
6. Read `docs/contracts/anti_slop_gate_contract.md`.
7. Read ADRs in `docs/decisions/`.
8. Read `docs/glossary.md` for canonical terms.

Milestone 0 completion does not require a dev server, database, migrations, or application tests.

## Milestone 1 Preparation

Before writing Milestone 1 code:

- identify the exact Milestone 1 phase and ticket;
- define scope, acceptance criteria, affected modules, and non-goals;
- define the relevant contracts before implementation;
- preserve source-of-truth boundaries from the product doctrine;
- include tests unless technically impossible;
- run checks in the order defined by `docs/testing.md`.

## Backend Development

Install dependencies:

```bash
python -m pip install -e ".[test]"
```

Run the API locally:

```bash
PYTHONPATH=backend uvicorn app.main:app --reload
```

Run migrations from the backend directory:

```bash
cd backend
PYTHONPATH=. alembic upgrade head
```

Run backend tests:

```bash
PYTHONPATH=backend python -m pytest backend/tests
```

Run full verification:

```bash
scripts/verify.sh
```

Create a Living Film Model artifact after creating a project and user:

```bash
curl -X POST http://localhost:8000/api/v1/projects/{project_id}/artifacts \
  -H "Content-Type: application/json" \
  -d '{"owner_user_id":"{user_id}","artifact_type":"creative_problem","title":"Creative Problem"}'
```

Append an artifact version:

```bash
curl -X POST http://localhost:8000/api/v1/artifacts/{artifact_id}/versions \
  -H "Content-Type: application/json" \
  -d '{"schema_version":"creative_problem.v1","author_user_id":"{user_id}","confidence_level":"medium","body":{"audience":"creative founders","objective":"define the creative problem","central_tension_or_opportunity":"AI video is easy to generate but hard to direct.","topic_vs_thesis":"The topic is AI video; the thesis is direction first.","constraints":["No script-to-video default."],"known_unknowns":["Which proof best shows the risk?"],"decision_owners":["creative owner"],"failure_definition":"The work becomes generic media assembly.","worth_producing_if":"It proves authored direction beats assembly."}}'
```

Create a decision:

```bash
curl -X POST http://localhost:8000/api/v1/projects/{project_id}/decisions \
  -H "Content-Type: application/json" \
  -d '{"owner_user_id":"{user_id}","title":"Select route","decision_text":"Choose the direction-first route.","alternatives_considered":["Direction-first route","Script assembly"],"selected_option":"Direction-first route","rationale":"It preserves source-of-truth boundaries.","affected_scope":{"artifacts":["{artifact_id}"]}}'
```

Change decision status:

```bash
curl -X PATCH http://localhost:8000/api/v1/decisions/{decision_id}/status \
  -H "Content-Type: application/json" \
  -d '{"status":"accepted"}'
```

Create a candidate creative input:

```bash
curl -X POST http://localhost:8000/api/v1/projects/{project_id}/creative-inputs \
  -H "Content-Type: application/json" \
  -d '{"submitted_by_user_id":"{user_id}","input_type":"script","title":"Submitted Script","body":{"raw_text":"Script candidate only."}}'
```

List candidate creative inputs:

```bash
curl http://localhost:8000/api/v1/projects/{project_id}/creative-inputs
```

Create a blackboard proof request:

```bash
curl -X POST http://localhost:8000/api/v1/projects/{project_id}/blackboard-entries \
  -H "Content-Type: application/json" \
  -d '{"author_user_id":"{user_id}","entry_type":"proof_request","title":"Need visual proof before production","summary":"The visual language is still an assumption.","rationale":"A production plan would be premature without checking the route.","confidence_level":"medium","severity":"high","payload":{"proof_type":"visual_language_test","question":"Can restrained product motion carry the thesis?","acceptance_test":"Reviewers can state the intended product feeling without narration.","cheapest_useful_proof":"Three still frames plus a 10 second motion sketch."}}'
```

Create a deliberation record:

```bash
curl -X POST http://localhost:8000/api/v1/projects/{project_id}/deliberations \
  -H "Content-Type: application/json" \
  -d '{"created_by_user_id":"{user_id}","phase":"decide","question":"What is the cheapest useful next proof?","priority_inputs":{"creative_impact":5,"uncertainty":4,"irreversibility":4,"cost_of_delay":3,"proof_cost":2,"dependency_blockage":5},"linked_entry_ids":["{blackboard_entry_id}"],"recommended_next_action":"Run the visual language proof before accepting treatment changes.","rationale":"The route has high downstream impact and a low-cost proof exists."}'
```
