# Creative Director OS — Build Plan and Milestone Roadmap

**Purpose:** This document turns the Creative Director OS architecture into a practical build journey: what to build first, what to delay, what each milestone must prove, and how the system should grow from a focused monolith into a complete studio-grade operating system.

**Core principle:** Do not start by building a video generator. Start by building the creative reasoning, editorial representation, proof workflow, and professional handoff system that prevent generic AI-slop output. Rendering is a capability; direction is the product.

---

## 1. The product you are actually building

The Creative Director OS is not a tool that receives a script and returns a video. It is a computational creative studio that helps a team decide what the work is, why it should exist, how the audience should experience it, what each audiovisual event must do, what proof is needed before production, and how assets, edits, reviews, and delivery stay connected to the original creative intent.

The system should eventually support creative directors, producers, editors, motion designers, sound designers, clients, and AI agents inside one shared operating layer. But the first version should be much narrower: one premium video workflow where the system proves it can reason, plan, prototype, edit, review, and improve quality better than a simple AI assembly pipeline.

The build journey should therefore move through four broad stages:

1. **Foundation Monolith:** prove the core creative data model, reasoning loop, and editorial score.
2. **Production Monolith:** connect the brain to assets, proofs, reviews, and NLE handoff.
3. **Studio Platform:** support multiple craft protocols, teams, permissions, integrations, and reusable formats.
4. **Creative Operating System:** become a full multi-role studio layer with calibrated taste, delegated production, and enterprise-grade reliability.

---

## 2. Architecture north star

Every milestone should protect the same final shape:

- **Studio Brain:** decides which creative problem should be solved next.
- **Living Film Model:** stores the evolving truth of the piece.
- **Audiovisual Score:** describes the intended viewer experience and editorial construction before it becomes a timeline.
- **Craft Protocols:** define the workflow for different kinds of videos.
- **Proof System:** forces risky ideas to become treatments, boards, animatics, edit tests, screenings, or prototypes before full commitment.
- **Execution Layer:** uses AI models, NLEs, design tools, renderers, and humans as tools, not as the source of truth.
- **Review and Learning Layer:** records what changed, why it changed, and whether the work improved.

The product stands out only if these layers remain separate. If the script becomes the timeline, the system becomes a normal AI video tool. If the model owns the final answer without proof, the system produces plausible rubbish. If the renderer becomes the center, the system will optimize for visual output rather than authored work.

---

## 3. Recommended technical stack

Start as a modular monolith. This is important. A distributed architecture too early will slow you down and hide product mistakes behind infrastructure complexity. The monolith should still have strict internal boundaries so it can later split into services if needed.

Recommended first stack:

- **Backend:** Python, FastAPI, Pydantic, SQLAlchemy, Alembic.
- **Database:** PostgreSQL with JSONB for typed creative artifacts and relational tables for projects, users, versions, assets, tasks, reviews, and permissions.
- **Object storage:** S3-compatible storage for media, boards, exports, proxies, transcripts, thumbnails, and renders.
- **Vector/search:** pgvector first; later move to dedicated vector/search infrastructure if scale demands it.
- **Workflow engine:** Temporal when workflows become durable and long-running; before that, simple job orchestration is acceptable.
- **Frontend:** TypeScript, React, a canvas/timeline-capable UI layer, and structured editing surfaces for treatments, boards, score lanes, reviews, and tasks.
- **Media tools:** FFmpeg, ffprobe, PyAV, OpenCV, OpenTimelineIO.
- **Preview/edit interchange:** Start with low-fidelity native preview plus OpenTimelineIO; integrate with Premiere first, then Resolve/Fusion later.
- **Planning/optimization:** OR-Tools CP-SAT for scheduling, resource planning, shot/task packing, and constraint solving.
- **AI model layer:** one strong reasoning model, one fast coordination/extraction model, VLMs for visual analysis, ASR/diarization, embedding/reranking models, and controlled image/video generation only for approved proof or production tasks.

The stack should be boring where possible. The originality belongs in the creative model, score, proof workflow, and brain — not in unnecessary infrastructure.

---

## 4. Build strategy

The dangerous path is to build a huge all-purpose creative suite first. That will take too long and still risk producing generic videos. The better path is to choose one demanding but narrow format, build the OS deeply for that format, then generalize.

The recommended first format is:

**Premium editorial/documentary-style video with narration, research, archival/reference material, designed graphics, sound direction, and professional NLE handoff.**

This format is ideal because it exposes the key problems:

- point of view matters;
- script alone is insufficient;
- visuals must be selected for editorial purpose;
- evidence and rights matter;
- sound and pacing matter;
- graphics must clarify, not decorate;
- the edit must be reviewed as an experience, not as a list of clips.

If the system can make this workflow intelligent, it can later expand into interviews, product films, ads, explainers, motion design, creator videos, internal comms, and synthetic/hybrid production.

---

## 5. Milestone 0 — Product definition and anti-slop constitution

**Goal:** Lock the product philosophy before writing too much software.

### Phase 0.1 — Define the operating thesis

Write the product thesis in one sentence:

> Creative Director OS is the system of record and reasoning layer for turning creative intent into authored audiovisual work.

Then define what the system is not:

- not a script-to-video generator;
- not a prompt wrapper;
- not a stock-footage assembler;
- not a replacement for editors;
- not a renderer-first product;
- not a generic project-management board with AI attached.

### Phase 0.2 — Define the anatomy of premium video

Create the quality model the system will enforce:

- point of view;
- audience movement;
- story or argument development;
- scene/sequence construction;
- visual logic;
- sound logic;
- edit logic;
- rhythm;
- specificity;
- restraint;
- finish.

This becomes the product’s creative constitution.

### Phase 0.3 — Define anti-slop rules

Add hard rules:

- no sentence-to-clip mapping as the default workflow;
- no generated or stock visual without an editorial role;
- no sequence without a formal idea;
- no final render without proof;
- no generic B-roll fallback;
- no self-approval by the same model that generated the idea;
- no “complete video” if the concept is weak.

### Exit criteria

You should have a written product doctrine, quality model, and refusal logic. If a future feature violates these rules, it should be rejected or redesigned.

---

## 6. Milestone 1 — Foundation monolith

**Goal:** Build the first working system of record for creative intent, structure, decisions, and versions.

### Phase 1.1 — Project and production model

Build the basic entities:

- workspace;
- user;
- project;
- production;
- piece;
- deliverable;
- asset;
- version;
- decision;
- task;
- review note.

Do not overbuild permissions yet. You need enough structure to support one team and one serious project.

### Phase 1.2 — Living Film Model v1

Implement typed artifacts:

- Creative Problem;
- Editorial Point of View;
- Audience Experience;
- Story/Argument Model;
- Direction Bible;
- Visual Language;
- Sound Direction;
- Production Constraints;
- Risk Register.

Each artifact needs:

- schema;
- version history;
- owner;
- confidence level;
- linked decisions;
- linked evidence;
- open questions.

### Phase 1.3 — Decision log

Build a first-class decision system. Every meaningful creative choice should capture:

- decision;
- alternatives considered;
- reason selected;
- evidence;
- risks;
- owner;
- status;
- what it affects.

This is one of the most important early features because it prevents the OS from becoming a chat history.

### Phase 1.4 — Creative brief ingestion

Allow users to input:

- raw brief;
- script;
- research notes;
- references;
- brand constraints;
- audience;
- deliverables;
- examples they like or dislike.

The system should extract structured candidates but not automatically treat them as truth. The user or Studio Brain must confirm important assumptions.

### Exit criteria

The system can create a project, ingest messy creative input, produce structured creative artifacts, track decisions, and maintain versions. No video generation is required yet.

---

## 7. Milestone 2 — Studio Brain v1

**Goal:** Build the reasoning controller that decides what creative problem should be solved next.

### Phase 2.1 — Blackboard architecture

Create a shared project blackboard where agents and tools can post:

- observations;
- proposals;
- contradictions;
- missing information;
- risks;
- proof requests;
- task recommendations.

The blackboard is not a chat room. It is structured working memory for the production.

### Phase 2.2 — Specialist proposal agents

Create early specialist agents:

- Creative Director Agent;
- Story/Argument Agent;
- Editorial Agent;
- Visual Direction Agent;
- Sound Direction Agent;
- Producer Agent;
- Critic Agent.

Each agent submits typed proposals. They should not directly mutate the source of truth. The brain decides what to accept, reject, or send for proof.

### Phase 2.3 — Deliberation controller

Build the controller that ranks next actions by:

- creative impact;
- uncertainty;
- irreversibility;
- production cost;
- schedule risk;
- cheapest useful proof;
- dependency blockage.

This is the “brain” of the OS. It should be able to say:

- “The script is not ready.”
- “We need a visual proof before production.”
- “The audience journey is unclear.”
- “The edit has rhythm but no point of view.”
- “This sequence needs evidence, not decoration.”

### Phase 2.4 — Human checkpoint protocol

Define where human approval is mandatory:

- project thesis;
- creative route;
- audience promise;
- final treatment;
- visual language;
- production plan;
- edit direction;
- final release.

### Exit criteria

The system can reason over a project, identify weaknesses, propose next actions, request proofs, and prevent premature production.

---

## 8. Milestone 3 — Audiovisual Score v1

**Goal:** Build the editorial source of truth that sits above the NLE timeline.

### Phase 3.1 — Score hierarchy

Implement:

- piece;
- act/movement;
- sequence;
- scene/segment;
- beat;
- shot/event;
- cut relationship.

Each timeline event should define:

- **Why:** viewer intent;
- **What:** narrative or audiovisual event;
- **How:** execution method, assets, movement, sound, capability;
- **Where/When:** placement, duration, timing, dependency.

### Phase 3.2 — Score lanes

Create coordinated lanes:

- audience state;
- story/argument;
- image;
- performance/voice;
- graphics;
- sound/music;
- rhythm;
- evidence;
- production state;
- review notes.

The user should be able to inspect why something exists in the timeline, not just where it sits.

### Phase 3.3 — Beat and cut logic

Model editorial relationships:

- reveal;
- contrast;
- continuation;
- interruption;
- escalation;
- compression;
- reaction;
- pause;
- payoff;
- transition;
- misdirection;
- evidence support.

This is where the system stops thinking like “clip assembly” and starts thinking like editing.

### Phase 3.4 — Low-fidelity preview

Build a simple preview system:

- cards;
- boards;
- scratch narration;
- temp stills;
- temp clips;
- music placeholders;
- timing;
- captions;
- rough transitions.

This preview does not need to look final. It needs to test whether the sequence works.

### Exit criteria

The system can produce a structured audiovisual score and a low-fidelity animatic/prototype that explains why each event exists.

---

## 9. Milestone 4 — Proof and pre-production system

**Goal:** Create the workflow that tests creative assumptions before expensive production.

### Phase 4.1 — Proof types

Implement proof artifacts:

- creative route;
- treatment;
- reference board;
- style frame;
- storyboard;
- animatic;
- edit test;
- sound sketch;
- graphics test;
- evidence pack;
- production feasibility test.

### Phase 4.2 — Risk-to-proof mapping

The brain should map risks to proof:

- unclear point of view → route comparison;
- weak story → treatment revision;
- uncertain visual world → moodboard/style frames;
- timing risk → animatic;
- graphics complexity → motion test;
- rights risk → evidence/asset clearance check;
- performance risk → voice or casting test;
- production risk → producer breakdown.

### Phase 4.3 — Approval gates

Build gates:

- idea approved;
- route approved;
- treatment approved;
- score approved;
- proof approved;
- production approved;
- edit approved;
- finishing approved.

The system may continue exploration before a gate, but it should not pretend a project is production-ready when core assumptions are unproven.

### Exit criteria

The system can identify risk, request the correct proof, store proof artifacts, and gate production decisions.

---

## 10. Milestone 5 — Asset and evidence intelligence

**Goal:** Build an asset system that understands creative role, rights, quality, and editorial usefulness.

### Phase 5.1 — Asset library

Support:

- uploads;
- proxies;
- thumbnails;
- transcripts;
- metadata;
- tags;
- rights;
- source;
- usage restrictions;
- project links.

### Phase 5.2 — Media analysis

Analyze:

- speech;
- speakers;
- scenes;
- objects;
- composition;
- motion;
- faces if legally allowed;
- text/OCR;
- quality issues;
- usable ranges;
- emotional or performance moments.

### Phase 5.3 — Editorial role tagging

Every useful asset range should be linked to a purpose:

- evidence;
- atmosphere;
- character;
- action;
- reaction;
- contrast;
- transition;
- motif;
- proof;
- texture;
- joke;
- tension;
- release.

This prevents the asset library from becoming a searchable pile of “related visuals.”

### Phase 5.4 — Evidence and rights layer

Track:

- source;
- license;
- expiry;
- geography;
- usage;
- citation;
- legal status;
- brand safety;
- factual confidence.

### Exit criteria

The system can ingest media, analyze it, link it to score events, and warn when an asset is creatively weak, legally unsafe, or editorially misused.

---

## 11. Milestone 6 — Professional NLE bridge

**Goal:** Let editors work in real tools while the OS remains the creative source of truth.

### Phase 6.1 — OpenTimelineIO export

Export:

- sequences;
- clips;
- markers;
- notes;
- placeholders;
- roles;
- lanes;
- temp audio;
- captions;
- references.

### Phase 6.2 — Premiere integration first

Build a Premiere panel or bridge that can:

- import OS sequences;
- show score intent beside the edit;
- sync markers and notes;
- report changes back;
- map clips to score events;
- flag unmotivated additions or missing required beats.

### Phase 6.3 — Edit change intelligence

When an editor changes the cut, the OS should ask:

- What changed?
- Which beat or intent changed?
- Was duration changed for rhythm or convenience?
- Did the change improve clarity?
- Did it break continuity?
- Does the score need updating?

### Phase 6.4 — Roundtrip workflow

Support:

- OS score to NLE;
- NLE edit to OS;
- OS review notes to NLE;
- NLE exports to OS;
- version comparison.

### Exit criteria

Editors can cut in Premiere while the OS tracks intent, structure, versions, notes, and changes.

---

## 12. Milestone 7 — Review, critique, and learning

**Goal:** Build a review system that improves the work instead of collecting vague comments.

### Phase 7.1 — Structured review

Review notes should capture:

- location;
- reviewer;
- observed issue;
- likely cause;
- severity;
- craft area;
- proposed action;
- related score event;
- status.

### Phase 7.2 — Screening mode

Create a review experience where viewers respond to:

- confusion;
- boredom;
- disbelief;
- emotional drop;
- attention loss;
- unclear claim;
- weak transition;
- overexplained moment;
- missing proof;
- sound or visual distraction.

### Phase 7.3 — Critic agents

Add specialist critique:

- audience clarity critic;
- story critic;
- editorial rhythm critic;
- visual coherence critic;
- sound critic;
- brand/client critic;
- factual/evidence critic.

Critics should not rewrite blindly. They should diagnose and propose fixes.

### Phase 7.4 — Learning from decisions

Record:

- what worked;
- what failed;
- recurring client preferences;
- format rules;
- editor patterns;
- brand taste;
- production bottlenecks.

This becomes the early taste memory of the OS.

### Exit criteria

The system can run structured reviews, diagnose problems, suggest fixes, and preserve learning across versions and projects.

---

## 13. Milestone 8 — Controlled AI production layer

**Goal:** Add AI generation as a controlled craft capability, not the center of the product.

### Phase 8.1 — Generation request contracts

Every generation request must include:

- score event;
- creative role;
- visual/sound constraints;
- continuity constraints;
- reference material;
- success criteria;
- rejection criteria;
- rights/provenance requirement.

### Phase 8.2 — Image and style-frame generation

Support generation for:

- visual exploration;
- reference boards;
- style frames;
- concept art;
- placeholder images;
- design directions.

These should be clearly marked as generated and should not automatically become final production material.

### Phase 8.3 — Video generation sandbox

Support video generation only for:

- approved shot ideas;
- previs;
- synthetic inserts;
- controlled background plates;
- motion tests;
- impossible or unaffordable shots.

Each generated clip must be evaluated for:

- continuity;
- usefulness;
- visual quality;
- rights/provenance;
- editorial fit;
- consistency with the direction bible.

### Phase 8.4 — Sound and music sketching

Support:

- temp music direction;
- sound sketches;
- sonic references;
- rhythm tests;
- narration timing;
- ambience concepts.

The system should avoid wallpaper music. Sound must have intent.

### Exit criteria

AI generation becomes a governed production capability that supports score events and proofs, not a shortcut around direction.

---

## 14. Milestone 9 — Producer OS

**Goal:** Add production planning, resources, constraints, and operational control.

### Phase 9.1 — Production breakdown

Convert the score into:

- asset needs;
- shoot needs;
- design needs;
- graphics needs;
- sound needs;
- rights needs;
- editing tasks;
- review tasks;
- finishing tasks.

### Phase 9.2 — Scheduling and dependencies

Track:

- owners;
- dates;
- dependencies;
- blockers;
- approvals;
- budget;
- capacity;
- delivery dates.

### Phase 9.3 — Cost and feasibility reasoning

The producer layer should ask:

- What is expensive?
- What is risky?
- What can be simplified?
- What needs human craft?
- What can be automated safely?
- What can be proven cheaply?
- What threatens delivery?

### Phase 9.4 — Vendor and human handoff packets

Generate packets for:

- editor;
- motion designer;
- sound designer;
- animator;
- researcher;
- producer;
- client reviewer;
- external studio.

Each packet should include intent, references, constraints, deliverables, and acceptance criteria.

### Exit criteria

The OS can convert creative direction into production tasks, schedules, handoffs, and feasibility decisions.

---

## 15. Milestone 10 — Multi-protocol studio platform

**Goal:** Expand beyond the first format into multiple professional workflows.

### Phase 10.1 — Protocol engine

Create a protocol system where each format defines:

- required artifacts;
- hierarchy;
- proof types;
- gates;
- craft lanes;
- agents;
- review criteria;
- production tasks;
- delivery requirements.

### Phase 10.2 — Add second protocol

Recommended second protocol:

**Interview-led brand/documentary film.**

This adds:

- transcript intelligence;
- character/story extraction;
- actuality scenes;
- interview selects;
- emotional continuity;
- performance;
- ethical representation.

### Phase 10.3 — Add third protocol

Recommended third protocol:

**Motion-design/product explainer.**

This adds:

- information design;
- typography;
- animation behavior;
- screen/product capture;
- graphic systems;
- layout consistency.

### Phase 10.4 — Protocol comparison and reuse

Allow teams to save:

- format bibles;
- channel rules;
- recurring structures;
- reusable score patterns;
- brand visual/sound rules;
- review rubrics.

### Exit criteria

The system can support multiple kinds of premium content without forcing every project into the same script-to-video pipeline.

---

## 16. Milestone 11 — Collaboration and studio operations

**Goal:** Make the system usable by real teams and studios.

### Phase 11.1 — Roles and permissions

Support:

- creative director;
- producer;
- editor;
- designer;
- sound;
- client;
- reviewer;
- admin.

Permissions should be based on creative responsibility, not only technical access.

### Phase 11.2 — Workspaces and accounts

Add:

- organizations;
- teams;
- project spaces;
- billing/account basics;
- templates;
- archive;
- audit logs.

### Phase 11.3 — Client review experience

Build a simple client-facing mode:

- watch;
- comment;
- approve;
- request change;
- compare versions;
- understand decisions at a high level.

Do not expose internal chaos to clients.

### Phase 11.4 — Notifications and task inbox

Support:

- assignments;
- review requests;
- blocked items;
- approvals;
- mentions;
- due dates;
- version updates.

### Exit criteria

The OS can be used by a small studio team across several real projects.

---

## 17. Milestone 12 — Advanced craft integrations

**Goal:** Integrate with more professional tools without losing the OS source of truth.

### Phase 12.1 — Resolve and color workflow

Support:

- Resolve import/export;
- color notes;
- LUT references;
- shot status;
- picture lock handoff;
- final conform tracking.

### Phase 12.2 — After Effects/Fusion workflow

Support:

- graphics requests;
- motion design specs;
- style frames;
- comp references;
- render status;
- version return.

### Phase 12.3 — Blender/Unreal workflow

Support:

- 3D shot requirements;
- camera/lens notes;
- previs;
- scene references;
- rendered plates;
- version tracking.

### Phase 12.4 — Audio workflow

Support:

- sound design briefs;
- music direction;
- stems;
- mix notes;
- loudness specs;
- final mix versions.

### Exit criteria

The OS coordinates professional craft surfaces while preserving creative intent, versions, and review state.

---

## 18. Milestone 13 — Quality intelligence and taste calibration

**Goal:** Make the system better at judging and improving work over time.

### Phase 13.1 — Quality rubrics

Build rubrics for:

- clarity;
- originality;
- pacing;
- specificity;
- visual coherence;
- sound integration;
- emotional movement;
- brand fit;
- evidence strength;
- production finish.

### Phase 13.2 — Taste profiles

Create taste memory for:

- studio;
- client;
- channel;
- director;
- editor;
- format.

This should not become a generic style preset. It should record actual preferences, rejected patterns, accepted choices, and creative principles.

### Phase 13.3 — Comparative critique

The system should compare:

- route A vs route B;
- cut version 3 vs version 4;
- different openings;
- different endings;
- different sound approaches;
- different graphic languages.

### Phase 13.4 — Outcome learning

Track real outcomes:

- client approval speed;
- revision count;
- audience retention;
- qualitative feedback;
- delivery accuracy;
- production overruns;
- recurring defects.

### Exit criteria

The OS can calibrate to a team’s taste and improve future recommendations based on real creative outcomes.

---

## 19. Milestone 14 — Enterprise and reliability layer

**Goal:** Prepare the system for serious studio adoption.

### Phase 14.1 — Security and compliance

Add:

- SSO;
- role-based access;
- audit logs;
- encryption;
- retention policies;
- data export;
- project isolation;
- rights documentation.

### Phase 14.2 — Scalability

Split only what needs to split:

- media processing workers;
- AI inference workers;
- workflow orchestration;
- search/indexing;
- render services;
- collaboration notifications.

Keep the core creative model coherent.

### Phase 14.3 — Observability

Track:

- failed jobs;
- slow workflows;
- expensive model calls;
- render failures;
- agent quality;
- user approval rates;
- revision cycles.

### Phase 14.4 — Disaster recovery

Add:

- backups;
- version restore;
- asset recovery;
- audit restore;
- project export;
- deployment rollback.

### Exit criteria

The system is safe enough for serious external studios to test with real projects.

---

## 20. Milestone 15 — Complete Creative OS

**Goal:** Reach the full vision: a creative operating system that can support premium content from idea to delivery.

### Phase 15.1 — Delegated studio operation

The OS can autonomously:

- diagnose briefs;
- propose routes;
- build treatments;
- create proof plans;
- assemble animatics;
- prepare edit packages;
- manage review cycles;
- produce production breakdowns;
- coordinate tool handoffs;
- flag weak work;
- request human decisions.

### Phase 15.2 — Multi-format production

Support:

- editorial/documentary;
- interview-led films;
- product explainers;
- motion design;
- ads;
- social campaigns;
- internal comms;
- education;
- synthetic/hybrid video;
- live-action support.

### Phase 15.3 — Studio marketplace layer

Optional later expansion:

- vetted editors;
- designers;
- sound designers;
- researchers;
- motion studios;
- voice talent;
- production vendors;
- specialized AI tools.

The OS can generate precise briefs and acceptance criteria for each contributor.

### Phase 15.4 — Creative intelligence memory

The OS becomes better across projects:

- format memory;
- client memory;
- brand memory;
- audience memory;
- craft memory;
- production memory;
- decision memory.

### Exit criteria

The OS can run a full creative production process while keeping human authorship, craft quality, and professional accountability intact.

---

## 21. Suggested build order summary

Build in this order:

1. Product doctrine and anti-slop rules.
2. Modular monolith foundation.
3. Living Film Model.
4. Decision log and versioning.
5. Studio Brain v1.
6. Audiovisual Score.
7. Low-fidelity preview.
8. Proof workflow.
9. Asset and evidence intelligence.
10. NLE bridge.
11. Structured review.
12. Controlled AI generation.
13. Producer OS.
14. Multiple craft protocols.
15. Collaboration and client review.
16. Advanced integrations.
17. Taste calibration.
18. Enterprise readiness.

The most important warning: do not build rendering too early. If the system cannot explain why a sequence exists, what the viewer should experience, what proof supports it, and how an editor should treat it, then better rendering will only create more polished slop.

---

## 22. MVP definition

The real MVP is not “generate a video.” The real MVP is:

> A user can bring a messy brief/script/reference set into the OS, and the system helps turn it into a strong creative route, treatment, audiovisual score, proof plan, rough animatic, asset plan, reviewable edit package, and NLE handoff — while preserving why every major creative decision exists.

Minimum MVP features:

- project setup;
- creative brief ingestion;
- Living Film Model v1;
- Studio Brain v1;
- decision log;
- audiovisual score;
- proof artifacts;
- asset library;
- low-fidelity animatic;
- OpenTimelineIO/Premiere handoff;
- structured review.

This is enough to prove the system is fundamentally different from AI video assembly.

---

## 23. First 90-day plan

### Days 1–15 — Doctrine and schemas

- finalize anti-slop constitution;
- define schemas for Living Film Model;
- define score hierarchy;
- define decision and review models;
- choose first protocol;
- design first UI surfaces.

### Days 16–35 — Monolith foundation

- backend setup;
- database setup;
- project model;
- artifact versioning;
- asset upload;
- decision log;
- basic frontend shell.

### Days 36–55 — Brain and score

- blackboard;
- specialist proposal agents;
- deliberation controller;
- score editor;
- score lanes;
- beat/event model.

### Days 56–75 — Proof and preview

- treatment generator;
- route comparison;
- proof requests;
- board/animatic preview;
- scratch narration;
- temp media placement;
- review notes.

### Days 76–90 — NLE handoff and pilot

- OpenTimelineIO export;
- Premiere import path;
- version comparison;
- one complete pilot project;
- quality review;
- roadmap adjustment.

At the end of 90 days, you should not expect a complete studio platform. You should expect a convincing proof that your OS thinks differently from AI video tools.

---

## 24. What to delay

Delay these until the core is proven:

- full native NLE;
- full compositor;
- full DAM/MAM replacement;
- marketplace;
- advanced billing;
- complex enterprise permissions;
- dozens of format protocols;
- autonomous end-to-end generation;
- custom video foundation models;
- deep 3D/Unreal workflows;
- huge client portals;
- complex microservices.

These are real features, but they are not first-order proof of the product.

---

## 25. What to measure

Measure whether the system produces better creative work and smoother production, not only faster output.

Important metrics:

- fewer unclear briefs;
- fewer revision loops;
- better first treatment approval;
- better edit clarity;
- fewer missing assets;
- fewer rights surprises;
- faster handoff to editor;
- stronger reviewer feedback;
- fewer generic visuals;
- more specific shot/asset choices;
- better continuity between concept and final edit.

The product wins if teams trust it as the place where creative truth lives.

---

## 26. Final build philosophy

The system should feel less like “AI makes video” and more like a very sharp creative producer sitting beside the team: remembering every decision, challenging weak ideas, asking for proof, organizing the work, protecting taste, helping editors, and keeping the project honest.

If you build the brain, score, proof system, and craft protocols first, the OS can become genuinely valuable. If you build the renderer first, the project will probably become another tool that outputs videos that look finished before they are actually directed.

