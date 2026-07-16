# ADR 0001 - Canonical Reference Architecture

**Status:** accepted  
**Date:** 2026-07-16

## Context

The project requires one standalone source of truth for system boundaries, layers, and invariants. AGENTS.md identifies `docs/creative_director_os_reference_architecture.md` as that source.

## Decision

`docs/creative_director_os_reference_architecture.md` is the canonical reference architecture for Creative Director OS.

The build plan, milestone docs, specs, contracts, decisions, tests, and implementation work must defer to that file when architecture boundaries or invariants conflict.

## Consequences

- Milestone and implementation work must preserve Studio Brain, Living Film Model, Audiovisual Score, Craft Protocols, Proof System, Execution Layer, and Review/Learning boundaries.
- Any later architecture change must update the canonical architecture or add a new ADR explaining the exception.
- Non-canonical architecture explorations must not be treated as system truth.
