# Decision Log API Contract

**Milestone:** 1  
**Phase:** 1.3 - Decision Log  
**Status:** implemented

## Purpose

The decision log prevents Creative Director OS from becoming chat history. Every meaningful creative choice is stored as a first-class, project-scoped record with rationale, alternatives, evidence, risk, owner, status, and downstream effect.

## Decision Fields

- `id`: UUID.
- `project_id`: existing project UUID.
- `owner_user_id`: existing user UUID.
- `target_artifact_id`: optional artifact UUID within the project.
- `target_artifact_version_id`: optional artifact version UUID within the project.
- `title`: non-empty string.
- `decision_text`: non-empty string describing the decision.
- `alternatives_considered`: non-empty list of alternatives.
- `selected_option`: selected alternative.
- `rationale`: non-empty reason for the selected option.
- `evidence`: list of evidence references.
- `risks`: list of risk descriptions.
- `affected_scope`: non-empty JSON object describing downstream effect.
- `status`: `proposed`, `accepted`, `rejected`, or `superseded`.
- `created_at`: timestamp.
- `updated_at`: timestamp.

## Routes

- `POST /api/v1/projects/{project_id}/decisions`
- `GET /api/v1/projects/{project_id}/decisions`
- `GET /api/v1/decisions/{decision_id}`
- `PATCH /api/v1/decisions/{decision_id}/status`

## Validation Rules

- Project must exist.
- Owner user must exist.
- Alternatives must not be empty.
- Selected option must match one alternative.
- Rationale must not be blank.
- Affected scope must not be empty.
- Evidence and risk list entries must not be blank.
- Target artifact, when supplied, must belong to the project.
- Target artifact version, when supplied, must belong to the project.
- If both target artifact and target artifact version are supplied, the version must belong to the target artifact.

## Status Rules

Supported statuses:

- `proposed`
- `accepted`
- `rejected`
- `superseded`

Status changes use the status route so they produce audit events.

## Artifact Version Links

Artifact versions may link to decisions through `linked_decisions`.

Linked decisions must:

- exist;
- belong to the same project as the artifact being versioned.

## Audit Rules

Audit events are written for:

- decision creation;
- decision status changes.

## Explicit Non-Goals

This phase does not implement:

- approval gate workflow;
- decision expiration;
- permission checks beyond existing owner references;
- review notes;
- task creation;
- Studio Brain decision routing;
- creative brief ingestion;
- rendering, NLE, or AI generation behavior.
