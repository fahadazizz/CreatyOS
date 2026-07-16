# Living Film Artifact Version API Contract

**Milestone:** 1  
**Phase:** 1.2 - Typed Artifact and Version Model  
**Status:** implemented

## Purpose

This contract defines the first durable Living Film Model artifact/version slice. It creates typed artifact records and append-only artifact versions before decision log and creative brief ingestion exist.

## Artifact Types

Supported artifact types:

- `creative_problem`
- `editorial_point_of_view`
- `audience_experience`
- `story_argument_model`
- `direction_bible`
- `visual_language`
- `sound_direction`
- `production_constraints`
- `risk_register`

`script` is intentionally not an artifact type. Script remains input only until a future ingestion phase stores it as an input candidate.

## Artifact Fields

- `id`: UUID.
- `project_id`: existing project UUID.
- `production_id`: optional existing production UUID within the project.
- `piece_id`: optional existing piece UUID within the project.
- `owner_user_id`: existing user UUID.
- `artifact_type`: one supported artifact type.
- `title`: non-empty string.
- `status`: currently `draft` on create.
- `created_at`: timestamp.
- `updated_at`: timestamp.

## Artifact Version Fields

- `id`: UUID.
- `artifact_id`: existing artifact UUID.
- `version_number`: append-only integer scoped to artifact.
- `schema_version`: non-empty schema version string.
- `author_user_id`: existing user UUID.
- `parent_version_id`: optional version UUID from the same artifact.
- `confidence_level`: `low`, `medium`, or `high`.
- `body`: non-empty JSON object.
- `linked_decisions`: list of decision UUIDs.
- `linked_evidence`: list of evidence references.
- `open_questions`: list of open question strings.
- `created_at`: timestamp.

## Routes

- `POST /api/v1/projects/{project_id}/artifacts`
- `GET /api/v1/projects/{project_id}/artifacts`
- `GET /api/v1/artifacts/{artifact_id}`
- `POST /api/v1/artifacts/{artifact_id}/versions`
- `GET /api/v1/artifacts/{artifact_id}/versions`

## Validation Rules

- Artifact type must be one supported Living Film Model v1 type.
- Artifact owner must be an existing user.
- Artifact project must exist.
- Optional production must belong to the artifact project.
- Optional piece must belong to the artifact project.
- If both production and piece are supplied, the piece must belong to the production.
- Version body must be a non-empty JSON object.
- Version schema version must be non-empty.
- Version confidence level must be `low`, `medium`, or `high`.
- Parent version, when supplied, must belong to the same artifact.
- Linked decisions must exist and belong to the artifact project.
- Open questions and linked evidence entries must not be blank.

## Versioning Rules

- Artifact versions are append-only.
- There is no update or delete route for artifact versions.
- `version_number` is assigned by the service as latest version plus one.
- Prior version bodies remain readable after a new version is appended.
- A version becomes durable source-of-truth only through explicit version creation.

## Audit Rules

Audit events are written for:

- artifact creation;
- artifact version creation.

## Explicit Non-Goals

This phase does not implement:

- evidence registry persistence;
- creative brief or script ingestion;
- schema-specific body validation beyond required non-empty JSON;
- approval gates;
- Studio Brain agents;
- review workflows;
- rendering, NLE, or AI generation behavior.
