# ADR 0005 - Foundation API Trusted Internal Boundary

**Status:** accepted  
**Date:** 2026-07-16

## Context

Milestone 1 establishes the Foundation Monolith system of record. The API currently accepts actor identifiers such as `owner_user_id`, `author_user_id`, and `submitted_by_user_id` in request bodies. There is no authentication or authorization middleware yet.

## Decision

Milestone 1 is production-ready only as an internal foundation slice under a trusted caller boundary. It must not be exposed as a public or multi-tenant API until an authentication and authorization phase defines actor context, role checks, and request attribution.

## Consequences

- Current tests validate data integrity, versioning, audit creation, and source-of-truth boundaries, not external access control.
- Future external deployment work must remove client-supplied actor authority and derive actor identity from authenticated request context.
- This ADR does not weaken audit requirements; it records the current boundary so later work does not mistake scaffold actor fields for a complete permission system.
