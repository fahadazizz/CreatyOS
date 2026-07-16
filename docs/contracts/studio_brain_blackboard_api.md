# Studio Brain Blackboard API Contract

**Milestone:** 2  
**Phase:** 2.1 - Blackboard Architecture  
**Status:** implemented

## Purpose

The Studio Brain blackboard stores structured working memory for a project. It lets tools, future agents, and humans record observations, proposals, contradictions, missing information, risks, issues, proof requests, and task recommendations without mutating Living Film Model artifacts, artifact versions, or decisions.

Deliberation records capture reasoning-control checkpoints over blackboard entries. They store the question, phase, priority inputs, linked entries, rationale, and recommended next action. They do not execute the action.

## Blackboard Entry Types

Supported entry types:

- `observation`
- `proposal`
- `contradiction`
- `missing_information`
- `risk`
- `issue`
- `proof_request`
- `task_recommendation`

Supported statuses:

- `open`
- `accepted`
- `rejected`
- `resolved`
- `superseded`

Supported severities:

- `low`
- `medium`
- `high`
- `critical`

## Blackboard Entry Fields

- `id`: UUID.
- `project_id`: existing project UUID.
- `author_user_id`: existing user UUID.
- `entry_type`: supported blackboard entry type.
- `title`: non-empty string.
- `summary`: non-empty string.
- `rationale`: non-empty string.
- `confidence_level`: `low`, `medium`, or `high`.
- `severity`: supported severity.
- `status`: controlled status, initially `open`.
- `payload`: non-empty JSON object with type-specific required fields.
- `target_artifact_id`: optional artifact UUID within the project.
- `target_artifact_version_id`: optional artifact version UUID within the project.
- `target_decision_id`: optional decision UUID within the project.
- `target_creative_input_id`: optional creative input UUID within the project.
- `created_at`: timestamp.
- `updated_at`: timestamp.

## Type-Specific Payload Requirements

- `observation`: `observation`, `evidence`.
- `proposal`: `proposal_type`, `recommended_action`, `expected_impact`.
- `contradiction`: `contradiction`, `conflicts_with`.
- `missing_information`: `question`, `needed_for`.
- `risk`: `risk_type`, `impact`, `mitigation`.
- `issue`: `issue_type`, `impact`, `mitigation`.
- `proof_request`: `proof_type`, `question`, `acceptance_test`, `cheapest_useful_proof`.
- `task_recommendation`: `task_type`, `recommended_owner`, `acceptance_criteria`.

## Deliberation Records

Supported phases:

- `sense`
- `frame`
- `diverge`
- `externalize`
- `experience`
- `critique`
- `decide`
- `commit`
- `propagate`
- `reopen`

Deliberation record fields:

- `id`: UUID.
- `project_id`: existing project UUID.
- `created_by_user_id`: existing user UUID.
- `phase`: supported deliberation phase.
- `question`: non-empty string.
- `priority_inputs`: object with `creative_impact`, `uncertainty`, `irreversibility`, `cost_of_delay`, `proof_cost`, and `dependency_blockage`, each scored 1 to 5.
- `linked_entry_ids`: blackboard entry UUIDs within the same project.
- `recommended_next_action`: non-empty string.
- `rationale`: non-empty string.
- `result`: optional JSON object.
- `status`: currently `open`.
- `created_at`: timestamp.
- `updated_at`: timestamp.

## Routes

- `POST /api/v1/projects/{project_id}/blackboard-entries`
- `GET /api/v1/projects/{project_id}/blackboard-entries`
- `GET /api/v1/blackboard-entries/{entry_id}`
- `PATCH /api/v1/blackboard-entries/{entry_id}/status`
- `POST /api/v1/projects/{project_id}/deliberations`
- `GET /api/v1/projects/{project_id}/deliberations`
- `GET /api/v1/deliberations/{deliberation_id}`

The blackboard list route supports optional filtering by `entry_type` and `status`.

## Validation Rules

- Project must exist.
- Author or creator user must exist.
- Blackboard entry payloads must satisfy type-specific required fields.
- Optional targets must belong to the blackboard entry project.
- If both artifact and artifact version targets are supplied, the artifact version must belong to that artifact.
- Deliberation linked entries must exist and belong to the deliberation project.
- Duplicate deliberation linked entry IDs are rejected.

## Source-of-Truth Rules

- Blackboard entries are working memory, not Living Film Model truth.
- Deliberation records are reasoning records, not approvals.
- Creating blackboard entries does not create or update artifacts, artifact versions, decisions, creative inputs, production records, or execution jobs.
- Creating deliberation records does not accept proposals, resolve proof requests, mutate decisions, or approve production.

## Audit Rules

Audit events are written for:

- blackboard entry creation;
- blackboard entry status changes;
- deliberation record creation.

## Explicit Non-Goals

Phase 2.1 does not implement:

- specialist agents;
- model calls;
- automatic proposal ranking;
- human approval checkpoints;
- task execution;
- rendering, NLE, review, or AI generation behavior.
