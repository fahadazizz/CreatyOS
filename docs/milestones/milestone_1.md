# Milestone 1 - Foundation Monolith

**Status:** complete  
**Canonical architecture:** `docs/creative_director_os_reference_architecture.md`  
**Build plan section:** Milestone 1 - Foundation monolith

## Goal

Build the first working system of record for creative intent, structure, decisions, and versions.

Milestone 1 must preserve the Milestone 0 doctrine: script is input only, durable artifacts are source of truth, and execution/rendering/generation are out of scope.

## Scope

In scope:

- backend app foundation;
- database and migrations;
- project, production, and piece basics;
- typed artifact model;
- version history;
- decision log;
- audit events;
- tests;
- docs and decisions when behavior or contracts change.

Out of scope:

- UI;
- Studio Brain agents;
- rendering;
- NLE bridge;
- AI generation;
- asset intelligence;
- review system.

## Phase 1.1 - Backend Foundation and Project Hierarchy

**Status:** implemented

### Outputs

- FastAPI backend app shell.
- SQLAlchemy database baseline.
- Alembic migration for project hierarchy tables.
- Project hierarchy entities:
  - workspace;
  - user;
  - project;
  - production;
  - piece;
  - deliverable.
- Audit event table and create-event writes.
- Pydantic request/response contracts.
- Service layer and API routes.
- Tests for hierarchy creation, validation, and audit events.

### Acceptance Criteria

- API can create a workspace and user.
- API can create a project owned by a user inside a workspace.
- API can create a production under a project.
- API can create a piece under a production.
- API can create a deliverable under a piece.
- API can list and fetch projects.
- API writes audit events for project, production, piece, and deliverable creation.
- Invalid foreign keys are rejected.
- Blank project titles are rejected by validation.

## Phase 1.2 - Typed Artifact and Version Model

**Status:** implemented

### Outputs

- Living Film Model artifact contracts for:
  - Creative Problem;
  - Editorial Point of View;
  - Audience Experience;
  - Story/Argument Model;
  - Direction Bible;
  - Visual Language;
  - Sound Direction;
  - Production Constraints;
  - Risk Register.
- Artifact and artifact version tables.
- Append-only version service.
- API routes for artifact create/read/version.
- Audit events for artifact and version writes.
- Tests for immutability, schema version recording, validation, and ownership.

### Acceptance Criteria

- Artifact versions are append-only.
- Each artifact version records schema version, owner, confidence, linked decisions, linked evidence, and open questions where relevant.
- Model/script inputs cannot become source of truth without explicit artifact version creation.
- Script is not an artifact type.
- Prior artifact versions remain readable after newer versions are appended.

## Phase 1.3 - Decision Log

**Status:** implemented

### Outputs

- Decision contracts and table.
- Decision service and API routes.
- Links from decisions to projects, artifacts, versions, and affected scope.
- Audit events for decision creation and status changes.
- Tests for alternatives, rationale, evidence, risks, owner, status, and affected scope.

### Acceptance Criteria

- Creative decisions are first-class records, not chat history.
- Each meaningful decision captures alternatives considered, reason selected, evidence, risks, owner, status, and downstream effect.
- Decision status changes produce audit events.
- Artifact versions can link only to decisions in the same project.

## Phase 1.4 - Creative Brief Ingestion Shell

**Status:** implemented

### Outputs

- Deterministic storage for raw brief, script, research notes, references, brand constraints, audience notes, deliverables, and examples.
- No AI extraction in this phase.
- Contracts that mark ingested inputs as candidates only.

### Acceptance Criteria

- Script and brief inputs are stored as inputs, never source of truth.
- Extracted or structured candidates cannot mutate Living Film Model artifacts without a later gate.
- Script is accepted as a creative input type but remains forbidden as a Living Film Model artifact type.
- Creative input creation writes audit events.

## Milestone Exit Criteria

Milestone 1 is complete. The system can create a project, ingest messy creative input as candidate-only records, produce structured Living Film Model artifacts, track decisions, and maintain append-only versions. No video generation is implemented or required.
