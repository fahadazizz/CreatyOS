# ADR 0003 - Script Is Input, Not Source Of Truth

**Status:** accepted  
**Date:** 2026-07-16

## Context

The product boundary requires Creative Director OS to avoid becoming a script-to-video generator. Scripts are useful inputs, but treating a script as timeline truth collapses creative direction into media assembly.

## Decision

Script is input only. It is never the timeline truth, creative source of truth, or automatic driver of clip search, generation, edit timing, or final approval.

The Living Film Model and Audiovisual Score hold the authoritative creative state. They may use script material, narration, transcript ranges, research notes, and evidence, but those inputs must be validated and intentionally adopted.

## Consequences

- Creative brief ingestion may extract candidates but must not automatically commit them as truth.
- Future workflows must reject sentence-to-clip defaults.
- Timeline projections and renders must trace back to approved score, intent, proof, and decisions rather than raw script sentences.
