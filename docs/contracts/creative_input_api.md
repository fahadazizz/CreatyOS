# Creative Input API Contract

**Milestone:** 1  
**Phase:** 1.4 - Creative Brief Ingestion Shell  
**Status:** implemented

## Purpose

Creative inputs store messy project material as candidate inputs only. They preserve raw brief, script, research, references, constraints, audience notes, deliverable notes, and examples without treating any input as Living Film Model truth.

This phase is deterministic. It performs no AI extraction and does not mutate artifacts, versions, decisions, or timeline state.

## Input Types

Supported input types:

- `raw_brief`
- `script`
- `research_notes`
- `reference`
- `brand_constraints`
- `audience_notes`
- `deliverables`
- `liked_example`
- `disliked_example`

## Fields

- `id`: UUID.
- `project_id`: existing project UUID.
- `production_id`: optional production UUID within the project.
- `piece_id`: optional piece UUID within the project.
- `submitted_by_user_id`: existing user UUID.
- `input_type`: supported input type.
- `title`: non-empty string.
- `source_label`: optional non-empty string.
- `candidate_state`: currently always `candidate`.
- `body`: non-empty JSON object.
- `created_at`: timestamp.

## Routes

- `POST /api/v1/projects/{project_id}/creative-inputs`
- `GET /api/v1/projects/{project_id}/creative-inputs`
- `GET /api/v1/creative-inputs/{creative_input_id}`

The project list route supports optional filtering by `input_type`.

## Validation Rules

- Project must exist.
- Submitted-by user must exist.
- Input type must be supported.
- Body must be a non-empty JSON object.
- Source label, when supplied, must not be blank.
- Optional production must belong to the project.
- Optional piece must belong to the project.
- If both production and piece are supplied, the piece must belong to the production.

## Source-of-Truth Rules

- Creative inputs are candidates only.
- Script is allowed as an input type but remains forbidden as a Living Film Model artifact type.
- Creating a creative input does not create or update artifacts.
- Creating a creative input does not create artifact versions.
- Creating a creative input does not create decisions.
- Promotion into source of truth requires explicit artifact/version creation in a separate workflow.

## Audit Rules

Audit events are written for creative input creation.

## Explicit Non-Goals

This phase does not implement:

- AI extraction;
- automatic candidate structuring;
- artifact mutation;
- approval gates;
- Studio Brain diagnosis;
- review notes;
- rendering, NLE, or AI generation behavior.
