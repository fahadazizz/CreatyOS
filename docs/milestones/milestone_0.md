# Milestone 0 - Product Doctrine and Anti-Slop Foundation

**Status:** complete for doctrine readiness  
**Source of truth:** `docs/creative_director_os_reference_architecture.md`  
**Supporting spec:** `docs/specs/product_doctrine_and_anti_slop.md`

## Goal

Create the product doctrine and anti-slop foundation before any software implementation.

Milestone 0 does not build application code, schemas, UI, agents, renderers, or integrations. It defines the product boundary, quality model, refusal logic, and review gates that all later milestones must preserve.

## Scope

In scope:

- define the operating thesis;
- define what the system is not;
- define the anatomy of premium authored video;
- define anti-slop invariants and refusal logic;
- define readiness gates for moving into Milestone 1;
- establish canonical vocabulary needed for Milestone 1 planning.

Out of scope:

- backend, frontend, model, database, or workflow implementation;
- Living Film Model schemas beyond doctrine-level naming;
- Audiovisual Score schema details;
- Studio Brain implementation;
- asset ingestion, rendering, NLE handoff, or media generation;
- broad rewrites of the reference architecture or build plan.

## Phase 0.1 - Operating Thesis

**Output:** product doctrine that states:

> Creative Director OS is the system of record and reasoning layer for turning creative intent into authored audiovisual work.

It also states that the system is not:

- a script-to-video generator;
- a prompt wrapper;
- a stock-footage assembler;
- a replacement for editors;
- a renderer-first product;
- a generic project-management board with AI attached.

**Acceptance criteria:**

- The thesis is documented in the product doctrine spec.
- Script is explicitly defined as input only, never timeline truth or creative source of truth.
- Rendering, generation, NLEs, humans, and AI models are defined as execution capabilities, not source of truth.

## Phase 0.2 - Anatomy of Premium Video

**Output:** quality model describing authored premium video across:

- point of view;
- audience movement;
- story or argument development;
- scene and sequence construction;
- visual logic;
- sound logic;
- edit logic;
- rhythm;
- specificity;
- restraint;
- finish.

**Acceptance criteria:**

- Quality is defined as authorship across craft systems, not cost, resolution, pace, or polish.
- The quality model can be used to reject decorative media assembly.
- The quality model preserves Why, What, How, and Where/When for audiovisual events.

## Phase 0.3 - Anti-Slop Constitution

**Output:** hard rules and refusal logic for preventing default AI-video assembly behavior.

The foundation must reject:

- sentence-to-clip mapping as the default workflow;
- generated or stock visuals without editorial role;
- sequences without formal ideas;
- final render before proof;
- generic B-roll fallback;
- self-approval by the same model that generated an idea;
- claiming a video is complete when thesis, evidence, direction, material, or execution quality fails the approved floor.

**Acceptance criteria:**

- Anti-slop rules are documented as invariants.
- Refusal outcomes are documented as blockers, revised scope, human craft requests, proof requests, or explicit compromise decisions.
- Future implementation work has a contract-level gate for checking these rules.

## Phase 0.4 - Milestone 1 Readiness

**Output:** readiness checklist for the Foundation Monolith.

Milestone 1 may start only when:

- the canonical architecture file remains the standalone system truth;
- the product doctrine and anti-slop spec is accepted;
- the gate contract exists for later implementation;
- glossary terms are available for core architecture names;
- testing and runbook docs define how doctrine-only milestones are verified.

**Acceptance criteria:**

- No application code has been written for Milestone 0.
- Milestone 1 can begin with Project/Production model and Living Film Model planning without revisiting product philosophy.
- Any future feature that violates the doctrine must be rejected, redesigned, or captured as an explicit ADR before implementation.

## Review Checklist

Before marking Milestone 0 complete, review for:

- architecture drift from the reference architecture;
- accidental script-to-video framing;
- confused source of truth between script, timeline, model output, and durable artifacts;
- missing gate or refusal behavior;
- invented terms not present in the glossary;
- implementation scope leaking into Milestone 0.

## Completion Summary

Milestone 0 guarantees that Creative Director OS starts as a creative reasoning and authored audiovisual work system, not a media assembly pipeline. It creates the doctrine, quality model, and anti-slop gates required before Milestone 1 can define durable project, production, artifact, decision, and version foundations.
