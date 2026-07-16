# ADR 0004 - Foundation Monolith Backend Stack

**Status:** accepted  
**Date:** 2026-07-16

## Context

Milestone 1 starts the Foundation Monolith. The build plan recommends Python, FastAPI, Pydantic, SQLAlchemy, Alembic, and PostgreSQL-compatible modeling while keeping the initial deployment modular rather than distributed.

The repository had no existing application source, so the first backend slice needed to establish a conservative app structure without building UI, agents, rendering, NLE integration, or AI generation.

## Decision

Use a Python FastAPI backend with Pydantic contracts, SQLAlchemy ORM models, and Alembic migrations.

The default local database URL is SQLite for development and tests, while the schema is kept simple enough to move to PostgreSQL in a later environment configuration.

## Consequences

- Backend slices must include contracts, service logic, API routes, validation, migrations, audit/version behavior when relevant, and tests.
- The modular monolith starts under `backend/app`.
- Milestone 1 Phase 1.1 implements project hierarchy and audit events only; typed artifacts, immutable versions, decision log, and ingestion remain separate bounded phases.
