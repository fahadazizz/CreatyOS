# Living Film Model v1

**Milestone:** 1  
**Phase:** 1.2 - Typed Artifact and Version Model  
**Status:** initial implementation

## Purpose

The Living Film Model is the source of truth for the authored work. It is a versioned family of typed artifacts and relationships, not a script, prompt, chat transcript, timeline, or rendered file.

This initial implementation creates the first durable artifact/version layer needed before decision log and ingestion behavior exist.

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

## Source-of-Truth Rule

A script, brief, prompt, model output, or note does not become Living Film Model truth by being submitted to the system. It becomes durable source-of-truth only when a typed artifact version is explicitly created and validated.

`script` is intentionally not an artifact type in Phase 1.2.

## Current Limits

Phase 1.2 validates artifact type, ownership, project scope, non-empty version body, schema version, confidence level, parent version scope, linked evidence text, and open question text.

It does not yet implement:

- schema-specific body validation for each artifact type;
- decision log persistence;
- evidence registry persistence;
- approval gates;
- creative brief ingestion;
- Studio Brain proposals;
- review workflows.
