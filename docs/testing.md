# Testing Strategy

## Milestone 0 Verification

Milestone 0 is docs-only, so application tests are not applicable.

Required verification:

- read `AGENTS.md`;
- read `docs/creative_director_os_build_plan.md`;
- read `docs/creative_director_os_reference_architecture.md`;
- verify the Milestone 0 docs preserve the product boundary;
- verify no application code was added or changed;
- verify the doctrine rejects script-to-video, renderer-first, and generic media assembly behavior;
- verify anti-slop gate outcomes include block, proof request, revise, escalate, and explicit compromise;
- verify glossary terms match canonical architecture names;
- review docs for contradictions before claiming completion.

## Future Implementation Check Order

When software implementation begins, run checks in this order when relevant:

1. unit tests;
2. integration/API tests;
3. type/lint checks;
4. `scripts/verify.sh`.

If a check is missing or technically impossible, document the gap in the final response and in the relevant milestone or runbook update.

## Milestone 1 Backend Checks

Install test dependencies before running backend tests:

```bash
python -m pip install -e ".[test]"
```

Run Phase 1 backend unit/API tests:

```bash
PYTHONPATH=backend python -m pytest backend/tests
```

Phase 1.2 artifact/version tests verify:

- artifact type validation;
- script is not a Living Film Model artifact type;
- version body validation;
- append-only version numbering;
- prior versions remain readable;
- artifact and artifact version audit events.

Run Alembic migrations:

```bash
cd backend
PYTHONPATH=. alembic upgrade head
```

## Anti-Slop Test Expectations

Future implementation tests should include boundary cases for:

- script sentences trying to create clip jobs directly;
- media with no designed role;
- final render request without proof;
- generic B-roll fallback;
- generated media self-approval;
- global score attempting to approve work;
- missing Why, What, How, or Where/When on an audiovisual event.
