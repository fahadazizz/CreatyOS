# ADR 0006 - Deterministic Studio Brain Blackboard

**Status:** accepted  
**Date:** 2026-07-16  
**Milestone:** 2.1 - Blackboard Architecture

## Context

Milestone 2 starts Studio Brain v1. The architecture requires a hierarchical blackboard where tools and future agents can post structured observations, proposals, contradictions, missing information, risks, proof requests, and task recommendations.

This must not become chat history, prompt transcript storage, or an agent framework as source of truth. Agents may propose later, but the system or human gates must approve mutations.

## Decision

Implement Phase 2.1 as deterministic backend infrastructure:

- `blackboard_entries` stores typed project working-memory records.
- `deliberation_records` stores reasoning-control checkpoints over blackboard entries.
- Entry payloads must satisfy type-specific required fields.
- Deliberation priority inputs are explicit numeric inputs, not hidden model scores.
- Blackboard targets and deliberation links are project-scoped.
- Writes produce audit events.
- Neither blackboard entries nor deliberation records mutate Living Film Model artifacts, artifact versions, decisions, creative inputs, production records, or execution records.

## Consequences

- Future specialist agents have a safe place to submit proposals without direct mutation.
- Future deliberation ranking can operate over structured records instead of chat text.
- Proof requests become first-class records before Proof System implementation.
- Human approval checkpoints remain a later phase and are not implied by deliberation records.

## Non-Goals

This decision does not add model calls, specialist agents, autonomous ranking, task execution, rendering, review, or UI.
