# Product Doctrine and Anti-Slop Spec

**Milestone:** 0  
**Status:** accepted foundation  
**Canonical architecture:** `docs/creative_director_os_reference_architecture.md`

## 1. Operating Thesis

Creative Director OS is the system of record and reasoning layer for turning creative intent into authored audiovisual work.

The product exists to preserve creative intent, proof, decisions, editorial reasoning, production state, and review learning across people, AI models, craft tools, media assets, and final deliveries.

## 2. Product Boundary

Creative Director OS is a computational creative studio. It helps a team decide what the work is, why it should exist, how the audience should experience it, what each audiovisual event must do, what proof is required before production, and how assets, edits, reviews, and delivery stay connected to approved creative intent.

It is not:

- a script-to-video generator;
- a prompt wrapper;
- a stock-footage assembler;
- a replacement for editors;
- a renderer-first product;
- a generic project-management board with AI attached.

The first workflow target is premium editorial/documentary-style video with narration, research, archival or reference material, designed graphics, sound direction, proof artifacts, review, and professional handoff.

## 3. Source-of-Truth Rules

The system source of truth is the durable, versioned creative and production record. The following are never source of truth by themselves:

- script;
- prompt;
- chat transcript;
- model memory;
- embedding result;
- generated media;
- NLE timeline;
- rendered file;
- analytics metric.

Script is input and evidence. It may inform a brief, treatment, score, narration, or review, but it is never timeline truth or the creative source of truth.

The timeline is an execution projection. The Audiovisual Score sits above the timeline and preserves intended viewer experience, editorial construction, audiovisual relationships, craft intent, proof state, and production bindings.

AI models, NLEs, renderers, design tools, media generators, search systems, and humans are execution or reasoning participants. They do not become authority merely because they produced the latest output.

## 4. Architecture Boundaries

Every milestone must preserve these system boundaries:

- **Studio Brain:** decides which creative problem or uncertainty should be solved next.
- **Living Film Model:** stores the evolving truth of the work as versioned typed artifacts and relationships.
- **Audiovisual Score:** describes intended viewer experience and editorial construction before timeline projection.
- **Craft Protocols:** define format-specific workflows, proofs, gates, and completion conditions.
- **Proof System:** requires risky ideas to become reviewable artifacts before expensive commitment.
- **Execution Layer:** uses AI models, NLEs, design tools, renderers, and humans as tools.
- **Review and Learning Layer:** records what changed, why it changed, whether the work improved, and what learning is ratified.

These boundaries are product invariants. A feature that collapses them must be rejected or redesigned.

## 5. Premium Video Quality Model

Premium means authored, not expensive. A premium video feels intentional at every scale: portfolio, piece, act, sequence, scene, beat, shot, cut, frame, and sample.

The product quality model has these dimensions:

- **Point of view:** the work has a specific relationship to its subject and audience.
- **Audience movement:** the viewer's knowledge, emotion, trust, attention, and memory change intentionally over time.
- **Story or argument development:** claims, evidence, questions, stakes, turns, and payoffs develop rather than merely continue.
- **Scene and sequence construction:** each substantial unit has a job, event, change, formal mode, progression, and transition logic.
- **Visual logic:** images, staging, graphics, composition, color, movement, and material specificity serve the governing idea.
- **Sound logic:** voice, ambience, effects, music, silence, dynamics, and transitions have dramatic or explanatory jobs.
- **Edit logic:** selections, durations, juxtapositions, reactions, reveals, ellipses, and cut relationships are motivated.
- **Rhythm:** change exists across acts, sequences, scenes, beats, shots, speech, motion, and music.
- **Specificity:** people, places, objects, actions, evidence, language, and media belong to this subject and route.
- **Restraint:** the work omits, pauses, simplifies, or leaves space when doing so strengthens the piece.
- **Finish:** typography, compositing, color, mix, captions, crops, delivery, and platform expression hold together.

Every audiovisual event must preserve:

- **Why:** viewer intent or creative purpose;
- **What:** narrative, evidential, emotional, formal, or audiovisual event;
- **How:** execution method, craft behavior, asset/material need, and sound/visual/edit logic;
- **Where/When:** placement, duration hypothesis, timing relationship, dependency, or branch.

## 6. Anti-Slop Invariants

These are hard product rules:

1. No sentence-to-clip mapping as the default workflow.
2. No media without a designed role.
3. No sequence without a formal idea.
4. No final production before proof.
5. No universal engagement pacing.
6. No duplicate channels by default.
7. No animation before design.
8. No generic B-roll as silent substitution.
9. No single-candidate acceptance for signature moments.
10. No generated continuity by prompt memory alone.
11. No music as emotional wallpaper.
12. No review by global score.
13. The system may refuse to finish.

## 7. Refusal Logic

The system must refuse, block, or escalate when a request would force a slop pattern.

Required refusal outcomes:

- **Creative gap:** no acceptable material, proof, route, or execution candidate exists.
- **Proof request:** the direction may be valid but needs treatment, board, style frame, sound sketch, animatic, edit test, screening, or feasibility proof.
- **Scope revision:** the ambition exceeds evidence, rights, budget, schedule, material, craft capability, or available proof.
- **Human craft request:** automated execution cannot satisfy the approved quality floor.
- **Decision gate:** accountable owner must approve, reject, delegate, or revise a high-impact decision.
- **Explicit compromise:** a known weakness is accepted with owner, reason, impact, scope, and downstream consequences.

The system must not hide refusal by substituting topic-adjacent footage, generic music, decorative text animation, unvalidated generated media, or a plausible but unproven final render.

## 8. AI Governance

AI agents and models propose. The system or accountable humans approve.

Model outputs must be:

- typed;
- validated;
- attributed to model/tool identity;
- stored intentionally;
- linked to input artifact versions;
- scoped by authority and risk;
- gated before mutating source of truth.

The same generator must never self-approve its own consequential output. Review findings must target specific artifacts, moments, rules, causes, and alternatives rather than a mysterious global quality score.

## 9. Milestone 1 Entry Gate

Milestone 1 may begin when future work accepts these non-negotiables:

- durable versioned artifacts outrank scripts, prompts, timelines, and renders;
- the Project/Production model must support decisions, versions, owners, review notes, and source-of-truth boundaries;
- Living Film Model v1 must express creative intent, not only production metadata;
- decision log is first-class, not chat history;
- ingestion may extract structured candidates but cannot automatically treat them as truth;
- tests for implementation milestones must include anti-slop boundary cases where relevant.

## 10. Non-Goals For Milestone 0

Milestone 0 does not define application code, database schema, API contracts, UI screens, media processing, model prompts, or NLE integration. Those start in later milestones only after their phase scope, contracts, implementation plan, and tests are explicit.
