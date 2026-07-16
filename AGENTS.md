# AGENTS.md — Creative Director OS

## 1. Product Boundary
- Build a Creative Director OS, not a script-to-video generator.
- Preserve: Studio Brain, Living Film Model, Audiovisual Score, Proof System, Execution Layer, Review/Learning.
- Script is input only; never timeline truth or creative source of truth.

## 2. Source of Truth
- Use docs to guide implementation, not replace implementation.
- Read only relevant docs: build plan, current milestone/phase, architecture, decisions, contracts, glossary, nearby code.
- Do not rediscover the whole repo every run.
- If context is missing, ask or document the assumption before writing.

## 3. Docs vs Code Rule
- Milestone 0 is docs/doctrine only.
- From Milestone 1 onward, default to production code first.
- Write docs only when contracts, architecture, setup, commands, decisions, or behavior change.
- Do not keep expanding docs while required code, tests, migrations, or APIs are missing.
- keep changes minimal: prefer short changelog/status bullets over long explanations atmost 2-3 lines.

## 4. Milestone Execution
- Strict chain: Milestone → Phase → Ticket → Contract → Implementation → Tests → Review.
- Never build a whole milestone in one run.
- Implement one bounded phase/ticket fully before moving on.
- Before coding, state scope, affected modules, acceptance criteria, and non-goals.

## 5. Build Rules
- No toy prototypes, fake flows, hardcoded outputs, placeholder production logic, or TODO-based core behavior.
- Backend slices must include schema/migration, contracts, services, API routes, validation, audit/versioning, tests, and docs updates when relevant.
- Frontend slices must include typed API usage, real state, loading/error/empty states, and no fake backend assumptions.
- If a referenced file like `scripts/verify.sh` is required but missing, create it or update the docs/rules to match reality.

## 6. AI/System Rules
- Separate deterministic logic from model calls.
- Model outputs must be typed, validated, stored intentionally, and gated before mutating source of truth.
- Agents propose; system or human gates approve.
- Never allow generator self-approval.

## 7. Anti-Slop Rules
- Never default to sentence-to-clip mapping, generic B-roll, wallpaper music, decorative text animation, or final render without proof.
- Every audiovisual event must preserve: Why, What, How, Where/When.

## 8. Preservation Rules
- Preserve public APIs, decision history, audit trails, migrations, tests, version behavior, and creative/production/execution boundaries.
- Do not rewrite architecture, schemas, or docs unless explicitly required.
- If a change risks breaking existing behavior, explain before implementing.

## 9. Testing Rules
- Tests are mandatory for implemented behavior unless technically impossible; document any gap.
- Run checks in order: unit → integration/API → type/lint → `scripts/verify.sh` if present.
- Do not claim completion without stating what passed, failed, or could not run.

## 10. Review Rules
- Before final response, review for architecture drift, invented assumptions, missing validation, missing tests, broken contracts, hardcoding, shallow logic, and unrelated edits.
- If task is ambiguous, large, destructive, or outside current phase, stop and ask.

## 11. Token Discipline
- Keep context clean: no huge logs, repeated stable docs, or unrelated scans.
- Prefer file references over restating docs.
- Use subagents only when explicitly requested or for independent read-heavy review, not overlapping edits.

## 12. Final Response
- Report only: what changed, files touched, tests run, decisions/docs updated, blockers, and next step.
