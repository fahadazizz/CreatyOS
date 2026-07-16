# Foundation Phase 1.1 API Contract

**Milestone:** 1  
**Phase:** 1.1 - Backend Foundation and Project Hierarchy  
**Status:** implemented

## Purpose

This contract defines the first backend slice for the Foundation Monolith. It creates the minimum durable project hierarchy needed before Living Film Model artifacts, versions, and decisions can be implemented.

## Entities

### Workspace

Fields:

- `id`: UUID.
- `name`: non-empty string.
- `slug`: unique lowercase URL-safe identifier.
- `created_at`: timestamp.
- `updated_at`: timestamp.

### User

Fields:

- `id`: UUID.
- `email`: unique normalized email-like string.
- `display_name`: non-empty string.
- `created_at`: timestamp.
- `updated_at`: timestamp.

### Project

Fields:

- `id`: UUID.
- `workspace_id`: existing workspace UUID.
- `owner_user_id`: existing user UUID.
- `title`: non-empty string.
- `logline`: optional string.
- `status`: currently `active` on create.
- `created_at`: timestamp.
- `updated_at`: timestamp.

### Production

Fields:

- `id`: UUID.
- `project_id`: existing project UUID.
- `title`: non-empty string.
- `format`: non-empty string.
- `status`: currently `development` on create.
- `created_at`: timestamp.
- `updated_at`: timestamp.

### Piece

Fields:

- `id`: UUID.
- `production_id`: existing production UUID.
- `title`: non-empty string.
- `runtime_target_seconds`: optional positive integer.
- `status`: currently `draft` on create.
- `created_at`: timestamp.
- `updated_at`: timestamp.

### Deliverable

Fields:

- `id`: UUID.
- `piece_id`: existing piece UUID.
- `name`: non-empty string.
- `platform`: non-empty string.
- `delivery_format`: non-empty string.
- `status`: currently `planned` on create.
- `created_at`: timestamp.
- `updated_at`: timestamp.

### Audit Event

Fields:

- `id`: UUID.
- `actor_user_id`: optional user UUID.
- `workspace_id`: optional workspace UUID.
- `project_id`: optional project UUID.
- `entity_type`: entity name.
- `entity_id`: entity UUID.
- `action`: event action.
- `payload`: JSON object.
- `created_at`: timestamp.

## Routes

- `POST /api/v1/workspaces`
- `POST /api/v1/users`
- `POST /api/v1/projects`
- `GET /api/v1/projects`
- `GET /api/v1/projects/{project_id}`
- `POST /api/v1/projects/{project_id}/productions`
- `POST /api/v1/productions/{production_id}/pieces`
- `POST /api/v1/pieces/{piece_id}/deliverables`
- `GET /api/v1/audit-events`

## Validation Rules

- Names, titles, formats, platforms, and delivery formats must not be blank.
- Project creation requires an existing workspace and owner user.
- Production creation requires an existing project.
- Piece creation requires an existing production.
- Deliverable creation requires an existing piece.
- Duplicate workspace slugs and duplicate user emails are conflicts.

## Audit Rules

Create events are written for:

- workspace;
- user;
- project;
- production;
- piece;
- deliverable.

Project-scoped audit queries return project, production, piece, and deliverable events associated with that project.

## Explicit Non-Goals

This phase does not implement:

- Living Film Model artifact versions;
- decision records;
- creative brief ingestion;
- permissions beyond ownership fields;
- review notes;
- tasks;
- assets;
- AI extraction;
- rendering or timeline behavior.
