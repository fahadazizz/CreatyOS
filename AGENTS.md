# AGENTS.md — Creative Director OS

## 1. Product Boundary
- Build a Creative Director OS, not a script-to-video generator.
- Preserve: Studio Brain, Living Film Model, Audiovisual Score, Proof System, Execution Layer, Review/Learning.
- Script is input only; never timeline truth or creative source of truth.
- `creative_director_os_reference_architecture.md` is standalone truth source for our system

## 2. Docs Map
- `docs/creative_director_os_build_plan.md`: milestone roadmap and build order.
- `docs/creative_director_os_reference_architecture.md`: system boundaries, layers, and invariants.
- `docs/milestones/`: one file per milestone with phases and acceptance criteria.
- `docs/specs/`: feature, data, API, agent, workflow, and UI-interface specs.
- `docs/contracts/`: schemas, API contracts, event contracts, model I/O contracts.
- `docs/decisions/`: ADRs for architecture/product decisions.
- `docs/testing.md`: test strategy, commands, fixtures, and verification rules.
- `docs/runbook.md`: setup, commands, debugging, operations.
- `docs/glossary.md`: canonical terms; do not invent alternate names.

## 3. Read Rules
- Read only docs relevant to the current task.
- Start with build plan → current milestone → current phase spec → architecture/decisions → nearby code.
- Use `docs/glossary.md` before inventing names or concepts.
- Do not rediscover the whole repo every run.
- If required context is missing, ask or document the assumption before writing.

## 4. Write Rules
- Write code only after scope, acceptance criteria, affected modules, and non-goals are clear.
- Write docs only when architecture, contracts, behavior, setup, commands, terms, or decisions change.
- Update milestone/phase docs when scope or completion status changes.
- Add/update ADRs in `docs/decisions/` for meaningful architecture/product choices.
- Do not rewrite architecture, schemas, migrations, tests, or docs unless explicitly required.

## 5. Milestone Pattern
- Strict chain: Milestone → Phase → Ticket → Contract → Implementation → Tests → Review.
- Never build a whole milestone in one run.
- Implement one bounded phase/ticket only.

## 6. Build Rules
- No toy prototypes, fake flows, hardcoded outputs, placeholder production logic, or TODO-based core behavior.
- Backend slices must include schema/migration, contracts, services, API, validation, audit/versioning, and tests when relevant.
- Frontend slices must include typed API usage, real state, loading/error/empty states, and no fake backend assumptions.

## 7. AI Rules
- Separate deterministic logic from model calls.
- Model outputs must be typed, validated, stored intentionally, and gated before mutating source of truth.
- Agents propose; system or human gates approve.
- Never allow generator self-approval.

## 8. Anti-Slop Rules
- Never default to sentence-to-clip mapping, generic B-roll, wallpaper music, decorative text animation, or final render without proof.
- Every audiovisual event must preserve: Why, What, How, Where/When.

## 9. Preservation Rules
- Preserve public APIs, decision history, audit trails, version behavior, and creative/production/execution boundaries.
- If a change risks breaking behavior, explain before implementing.

## 10. Testing Rules
- Tests are mandatory unless technically impossible; document any gap.
- Run checks in order: unit → integration/API → type/lint → `scripts/verify.sh`.
- Do not claim completion without stating what passed or failed.

## 11. Review Rules
- Before final response, review for architecture drift, invented assumptions, missing validation, missing tests, hardcoding, and unrelated edits.
- If task is ambiguous, large, destructive, or outside current phase, stop and ask.

## 12. Token Discipline
- Keep context clean: no huge logs, repeated stable docs, or unrelated repo scans.
- Use subagents only when explicitly requested or for independent read-heavy review.

## 13. Final Response
- Report only: changes made, files touched, tests run, decisions added, blockers, and next step.
