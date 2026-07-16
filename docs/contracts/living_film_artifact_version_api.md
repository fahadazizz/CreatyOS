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
- `body`: artifact-type-specific JSON object matching the active schema version.
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
- Version schema version must match the artifact type.
- Version confidence level must be `low`, `medium`, or `high`.
- Parent version, when supplied, must belong to the same artifact.
- Linked decisions must exist and belong to the artifact project.
- Open questions and linked evidence entries must not be blank.
- Unknown body fields are rejected.

## Body Schemas

Supported schema versions and required body fields:

- `creative_problem.v1`: `audience`, `objective`, `central_tension_or_opportunity`, `topic_vs_thesis`, `constraints`, `known_unknowns`, `decision_owners`, `failure_definition`, `worth_producing_if`.
- `editorial_point_of_view.v1`: `position`, `claims_or_questions`, `certainty`, `source_basis`, `narrator_position`, `audience_relationship`, `ethical_stance`, `counter_position`, `tonal_contract`.
- `audience_experience.v1`: `entry_state`, `desired_exit_state`, `evolving_questions`, `emotional_curve`, `attention_targets`, `trust_risks`, `memory_anchors`.
- `story_argument_model.v1`: `premise`, `controlling_question`, `stakes`, `payoff`, `claims`, `evidence_dependencies`, `counterclaims`, `turns`, `omitted_paths`.
- `direction_bible.v1`: `governing_formal_idea`, `point_of_view_distance`, `sequence_modes`, `visual_principles`, `sound_principles`, `performance_principles`, `tempo_and_restraint`, `signature_moments`, `anti_vision`.
- `visual_language.v1`: `framing_logic`, `camera_behavior`, `composition_rules`, `lighting_color_texture`, `motifs`, `transition_principles`, `rule_break_conditions`.
- `sound_direction.v1`: `listening_perspective`, `narration_relationship`, `ambience_strategy`, `music_function`, `silence_strategy`, `sonic_motifs`, `transition_rules`, `accessibility_requirements`.
- `production_constraints.v1`: `budget_constraints`, `schedule_constraints`, `legal_constraints`, `brand_constraints`, `capability_constraints`, `delivery_requirements`, `explicit_tradeoffs`.
- `risk_register.v1`: `risks`, `impact`, `likelihood`, `mitigations`, `proof_needed`, `owner`, `status`.

String fields must not be blank. List fields must contain at least one non-blank item.

## Versioning Rules

- Artifact versions are append-only.
- There is no update or delete route for artifact versions.
- `version_number` is assigned by the service as latest version plus one.
- Unique version-number conflicts return `409` so clients can retry version creation.
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
- approval gates;
- Studio Brain agents;
- review workflows;
- rendering, NLE, or AI generation behavior.
