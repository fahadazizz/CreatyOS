# ADR 0002 - Milestone 0 Is Docs-Only Doctrine Work

**Status:** accepted  
**Date:** 2026-07-16

## Context

The build plan defines Milestone 0 as product definition and anti-slop constitution. The goal is to lock product philosophy before writing too much software.

Starting code before the doctrine, quality model, and refusal logic are documented would risk building a script-to-video or renderer-first system.

## Decision

Milestone 0 creates and updates documentation only.

It may create milestone docs, doctrine specs, product contracts, glossary entries, testing notes, runbook notes, and ADRs. It must not write application code, database schema, UI, agents, prompts, model workflows, renderers, or integrations.

## Consequences

- Milestone 1 starts only after Milestone 0 doctrine is reviewable.
- Implementation tests are not applicable to Milestone 0, but documentation consistency review is mandatory.
- Later software work must reference the Milestone 0 doctrine and anti-slop contract when defining scope and acceptance criteria.
