# Milestone 2 - Studio Brain v1

**Status:** in progress  
**Canonical architecture:** `docs/creative_director_os_reference_architecture.md`  
**Build plan section:** Milestone 2 - Studio Brain v1

## Goal

Build deterministic reasoning-control infrastructure for the Studio Brain. Milestone 2 must help the system decide what creative problem should be solved next without allowing agents, model calls, or generators to mutate source of truth.

## Scope

In scope:

- project blackboard;
- structured observations, proposals, contradictions, missing information, risks, issues, proof requests, and task recommendations;
- deliberation records;
- future specialist proposal contracts;
- future human checkpoint protocol.

Out of scope:

- UI;
- Studio Brain model calls;
- autonomous specialist agents;
- rendering;
- NLE bridge;
- AI generation;
- review system.

## Phase 2.1 - Blackboard Architecture

**Status:** implemented

### Outputs

- Blackboard entry table and migration.
- Deliberation record table and migration.
- Type-specific Pydantic contracts for blackboard payloads.
- API routes for create/list/get/status update.
- Project-scoped target validation for artifact, artifact version, decision, and creative input links.
- Audit events for blackboard entry creation, blackboard status change, and deliberation record creation.
- Tests for validation, filtering, audit events, cross-project rejection, and no source-of-truth mutation.

### Acceptance Criteria

- API can create structured blackboard entries for all Phase 2.1 entry types.
- API rejects vague proof requests and other entries missing type-specific payload fields.
- API can list and filter blackboard entries by type and status.
- API can update blackboard entry status with an audit event.
- API can create deliberation records linked to project-local blackboard entries.
- Deliberation records store phase, question, priority inputs, rationale, and recommended next action.
- Blackboard and deliberation writes do not create or update artifacts, artifact versions, decisions, creative inputs, or execution records.

## Phase 2.2 - Specialist Proposal Agents

**Status:** implemented

- Supports deterministic specialist proposal submission for the seven planned specialist roles.
- Each proposal creates a linked blackboard `proposal` entry.
- Proposals are listable/filterable and audited.
- No proposal mutates source-of-truth records or runs a model.

## Phase 2.3 - Deliberation Controller

**Status:** implemented

- Deterministically ranks open blackboard entries by priority inputs.
- Creates a recorded deliberation record for the selected next action.
- Does not accept proposals, approve work, call models, or mutate source-of-truth records.

## Phase 2.4 - Human Checkpoint Protocol

**Status:** not started

## Milestone Exit Criteria

Milestone 2 is not complete. Phase 2.1 provides the deterministic blackboard and deliberation record foundation. Remaining work must add specialist proposal infrastructure, deliberation ranking/control behavior, and mandatory human checkpoint protocol before Milestone 2 can be considered complete.
