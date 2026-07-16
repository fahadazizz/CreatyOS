# Living Film Model v1

**Milestone:** 1  
**Phase:** 1.2 - Typed Artifact and Version Model  
**Status:** initial implementation

## Purpose

The Living Film Model is the source of truth for the authored work. It is a versioned family of typed artifacts and relationships, not a script, prompt, chat transcript, timeline, or rendered file.

This initial implementation creates the first durable artifact/version layer, decision log, and candidate-only creative input storage.

## Implemented Artifact Types

Living Film Model v1 supports these artifact types:

- `creative_problem`
- `editorial_point_of_view`
- `audience_experience`
- `story_argument_model`
- `direction_bible`
- `visual_language`
- `sound_direction`
- `production_constraints`
- `risk_register`

## Artifact Contract

An artifact is a stable typed record scoped to a project. It may optionally be scoped to a production or piece.

Required properties:

- project;
- owner;
- artifact type;
- title;
- status;
- created and updated timestamps.

## Version Contract

Artifact versions are append-only.

Each version records:

- artifact;
- version number;
- schema version;
- author;
- optional parent version;
- confidence level;
- JSON body;
- linked decisions;
- linked evidence;
- open questions;
- creation timestamp.

The system assigns version numbers. Clients cannot overwrite prior versions.

Linked decisions must exist and belong to the same project as the artifact.

## Decision Log

Decisions are first-class project-scoped records. They capture:

- owner;
- optional target artifact;
- optional target artifact version;
- decision text;
- alternatives considered;
- selected option;
- rationale;
- evidence;
- risks;
- affected scope;
- status;
- created and updated timestamps.

Decision records prevent creative choices from being buried in chat history. Artifact versions may link to accepted, proposed, rejected, or superseded decisions so later phases can trace source-of-truth changes to their rationale.

## Creative Inputs

Creative inputs store messy material as candidates only:

- raw brief;
- script;
- research notes;
- references;
- brand constraints;
- audience notes;
- deliverable notes;
- liked examples;
- disliked examples.

Creative inputs are not Living Film Model artifacts. Creating one does not create an artifact, create a version, create a decision, or mutate source of truth.

## Source-of-Truth Rule

A script, brief, prompt, model output, or note does not become Living Film Model truth by being submitted to the system. It becomes durable source-of-truth only when a typed artifact version is explicitly created and validated.

`script` is intentionally not an artifact type. It is allowed only as a candidate creative input.

## Current Limits

Phase 1 validates artifact type, ownership, project scope, non-empty version body, schema version, confidence level, parent version scope, linked decision scope, linked evidence text, open question text, decision alternatives, rationale, selected option, status, evidence, risk, affected scope, creative input type, and creative input candidate body.

It does not yet implement:

- schema-specific body validation for each artifact type;
- evidence registry persistence;
- approval gates;
- AI extraction from creative inputs;
- Studio Brain proposals;
- review workflows.
