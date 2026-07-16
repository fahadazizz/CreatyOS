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
