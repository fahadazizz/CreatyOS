# Creative Director OS — Fundamental Reference Architecture

**Status:** complete replacement of the prior architecture  
**Date:** 2026-07-16  
**Scope:** the creative reasoning brain, living film representation, real editorial stack, craft workflows, execution interfaces, component boundaries, technology stack, triggers, evaluation system, and build order required for a Creative OS that can support authored premium video instead of automated media assembly.

## 0. The correction

The previous architecture was wrong at its center. It added governance, traceability, rights, versioning, and better semantics around a familiar AI-video pipeline, but the pipeline was still essentially:

> intent and script → find or generate media → arrange media on tracks → render → review

That is a controlled assembly system. It may produce competent informational video, but its natural output is still narration covered by footage, generated clips, kinetic text, stock transitions, and decorative motion. More metadata does not turn that process into direction. Better review does not create a film grammar that was never designed.

The replacement architecture begins from how authored audiovisual work is actually constructed. Professionals externalize the work at several levels of fidelity: premise, treatment, story structure, visual development, storyboards, color scripts, shot design, blocking, style frames, sound concepts, animatics, dailies, assemblies, rough cuts, screenings, fine cuts, picture lock, sound, color, and finishing. Those are not bureaucratic artifacts. Each is a different instrument for discovering whether the work functions before the next class of expensive decisions becomes difficult to reverse.

The new OS is built around four core systems:

1. **Studio Brain:** a hierarchical, blackboard-style deliberation system that decides which creative problem should be solved next, which specialist reasoning or craft capability should address it, and what proof is sufficient before commitment.
2. **Living Film Model:** the authoritative, evolving representation of the work from thesis and audience experience down to scenes, shots, performance, sound, graphics, production state, and variants.
3. **Audiovisual Score:** the multi-resolution editorial representation that models relationships across time—story, performance, image, sound, graphics, rhythm, continuity, and viewer orientation—before projecting them into an NLE timeline.
4. **Craft Protocols and Runtimes:** format-specific creative methods and execution environments for documentary, live action, interviews, motion design, product/screen work, animation, virtual production, and hybrids.

The system is therefore not “an AI that makes a video.” It is a computational studio that can reason, prototype, direct, produce, edit, finish, and learn while keeping human authorship and professional craft surfaces available wherever automation is not yet good enough.

## 1. Anatomy of premium video

Premium does not mean expensive, cinematic LUTs, 3D particles, fast cuts, or a high-resolution render. It means the work feels authored at every scale. The viewer experiences one intentional piece rather than a sequence of plausible media outputs.

### 1.1 The six properties of authored work

#### Coherence

Story, image, performance, sound, graphics, rhythm, and finish express the same governing idea while contributing different information. Coherence is not visual uniformity. It permits contrast and surprise, but the contrast has a reason.

#### Specificity

People, places, objects, actions, language, sounds, visual evidence, and design choices belong to this exact subject and point of view. Generic footage of “a worried person,” a random data animation, or an AI-generated city may be topically related yet dramatically useless.

#### Development

Information, emotion, power, visual motifs, sound, scale, tempo, and expectation change through time. Premium work does not merely continue; it develops. Repetition returns with a changed meaning or intensity.

#### Selection

The work contains less than the creator could have included. Shots end at intentional moments. Music enters and leaves. Graphics appear only when they clarify or transform. Silence, reaction, empty space, and restraint are selected as actively as visible material.

#### Integration

Picture does not illustrate every word, music does not indiscriminately manufacture emotion, text does not repeat narration, and motion does not decorate static design. The crafts interact: an edit may begin in sound; a performance may motivate a camera move; production design may carry information that removes exposition.

#### Finish

The work survives close attention. Typography, compositing, color, dialogue, ambience, transitions, pacing, graphics, captions, crops, and delivery all feel like the same piece. Finish cannot rescue a weak concept, but weak finish can destroy a strong one.

### 1.2 The twelve coupled craft systems

A premium video is the interaction of at least twelve systems. A project may emphasize some and minimize others, but it cannot pretend they do not exist.

1. **Editorial point of view:** what the work believes, notices, questions, or refuses to simplify.
2. **Audience experience:** how knowledge, emotion, expectation, attention, and trust should change over time.
3. **Dramaturgy or argument:** causality, conflict, stakes, questions, evidence, revelations, turns, and payoffs.
4. **Scene construction:** the objective, event, change, point of view, spatial situation, and transition of each scene or designed sequence.
5. **Performance:** voice, behavior, character objective, subtext, delivery, gesture, timing, reaction, and presence—even narration and typography perform.
6. **Mise-en-scène and production design:** world, space, objects, costume, texture, palette, light sources, graphics in the environment, and meaningful absence.
7. **Cinematography:** staging, blocking, framing, lens/perspective, camera height, movement, focus, light, exposure, color, and what is withheld outside the frame.
8. **Editorial construction:** selection, juxtaposition, continuity, ellipsis, montage, reaction, reveal, repetition, duration, and cut motivation.
9. **Sound and music:** perspective, dialogue, narration, ambience, effects, silence, musical structure, dynamics, spatiality, and transitions.
10. **Graphic and motion language:** composition, typography, hierarchy, information design, spatial logic, animation behavior, and integration with footage.
11. **Rhythm:** change across acts, sequences, scenes, beats, shots, gestures, speech, motion, and music—not merely cuts per minute.
12. **Finishing and delivery:** VFX, compositing, color, mix, titles, captions, localization, mastering, and platform-specific expression.

The architecture must give every relevant craft an explicit place to reason and an explicit contract with the others. “Add B-roll here” is not a substitute for scene construction, cinematography, or editorial reasoning.

### 1.3 The anatomy operates at multiple scales

Premium quality is fractal. The same piece must work at:

- **Portfolio scale:** why this work belongs to the channel, programme, brand, or creator.
- **Piece scale:** the governing premise, formal idea, emotional movement, and total experience.
- **Act or movement scale:** the large changes in question, power, knowledge, or energy.
- **Sequence scale:** a sustained dramatic or explanatory movement with its own formal logic.
- **Scene scale:** an event in a place, time, argument, performance, or designed visual world that creates a change.
- **Beat scale:** the smallest change in thought, feeling, objective, information, or action.
- **Shot scale:** a designed unit of point of view, performance, space, duration, and sound.
- **Cut scale:** a relationship between outgoing and incoming image/sound, not simply the end of a clip.
- **Frame and sample scale:** composition, eye trace, motion phase, sync, texture, dynamics, and technical finish.

An LLM may create locally plausible beats while the piece fails at sequence or act level. Research on long-form generation repeatedly identifies the difficulty of maintaining macro-level planning and long-range consistency; hierarchical plans help, but static plans also fail when they are not revised during generation. The OS therefore requires dynamic hierarchical planning rather than one outline followed by one long generation pass.

### 1.4 Why contemporary AI video becomes slop

The common pipeline optimizes local plausibility:

- one script sentence produces one visual query or prompt;
- the best-looking local result is selected;
- clips inherit no shared world, camera grammar, performance logic, or developing motif;
- voiceover supplies all causality while image supplies topical motion;
- music supplies undifferentiated emotional continuity;
- text and shapes conceal the absence of scene construction;
- pace is increased to prevent the viewer noticing that nothing develops;
- quality checks measure visual defects, not authorship.

Even current multi-shot video research treats cross-shot identity, background, and temporal consistency as active technical problems. Visual consistency alone still does not supply direction, but its absence makes long synthetic sequences visibly incoherent. The OS must therefore treat generated video as one volatile material source inside a directed production, not as the production method by default.

## 2. The product: a computational creative studio

### 2.1 What the OS owns

The OS owns the continuity of creative reasoning and production state across tools and people. It should be able to answer:

- What is the central creative problem?
- Which alternative directions were considered and why was one selected?
- What should the audience experience at this point?
- What does this sequence do that no other sequence does?
- Why is the scene staged, shot, voiced, designed, sounded, and edited this way?
- Which choices are fixed, which remain hypotheses, and which are blocked?
- What is the cheapest artifact that could test the risky assumption?
- Which material or take fulfills the design, and what is missing?
- What changed in the cut, and which earlier decisions should be revisited?
- Which craft application owns the editable execution, and how is it synchronized?
- What did a reviewer actually experience, and is the cause known or merely suspected?

### 2.2 What the OS must not attempt to own initially

It should not initially reimplement every mature craft application. A standalone studio system does not require a standalone replacement for Premiere, Resolve, Fusion, After Effects, Blender, Unreal, Pro Tools, or every camera and production workflow. Professional studios are systems of interoperating craft surfaces. Rebuilding all of them would consume the project while producing worse tools for artists.

The OS needs its own reasoning, artifacts, production state, low-fidelity preview, review, and bounded automated renderer. It should integrate bidirectionally with professional NLEs, DCCs, audio tools, and renderers for execution. A native high-end NLE or compositor should be built only after the semantic and craft model is proven and a specific integration limitation justifies it.

### 2.3 Three classes of user benefit

#### Non-expert creator

The creator does not need to become a producer, storyboard artist, editor, or motion designer. They react to meaningful alternatives, prototypes, and screenings. The OS converts those judgments into durable direction and coordinates execution.

#### Professional creative team

Directors, producers, editors, designers, sound teams, and clients retain their craft tools while gaining a shared film model, decision ancestry, production-aware prototypes, precise change propagation, and fewer contradictory handoffs.

#### Delegated studio operation

After a format and taste model are calibrated, the system can autonomously solve routine problems, commission or generate material, assemble prototypes, prepare edit branches, and deliver release candidates. It escalates high-impact uncertainty rather than silently producing a complete but mediocre video.

## 3. The Living Film Model

The Living Film Model is the source of truth for the authored work. It is not one JSON document, one graph, one script, or one timeline. It is a versioned family of typed artifacts and relationships that describe the film at multiple resolutions.

### 3.1 Core hierarchy

The structural hierarchy is:

- Studio / creator
- Channel / brand
- Programme / campaign
- Series / format
- Commission
- Production
- Piece
- Act / movement / chapter
- Sequence
- Scene or designed segment
- Beat
- Shot or graphic/sound event
- Element / frame / sample range
- Deliverable variant

Not every format uses “act” or “scene” in the same way. The hierarchy supports typed units defined by the active Craft Protocol. A motion-design piece may use movements and boards; a documentary may use chapters, thematic sequences, and actuality scenes; a product demo may use user goals and interaction sequences.

### 3.2 Creative Problem Model

This artifact holds the commission as a problem to solve:

- audience and situation;
- desired effect and business/editorial objective;
- central tension or opportunity;
- topic versus actual thesis;
- deliverables and platform context;
- evidence, legal, cultural, brand, budget, schedule, and capability constraints;
- known unknowns;
- accountable owner and delegated authority;
- what failure would look like;
- what would make the work worth producing.

The system may challenge the commission. If the supplied script has no original point of view, a new renderer is not the answer.

### 3.3 Editorial Point-of-View Model

This records the work’s relationship to its subject:

- what it claims, investigates, dramatizes, demonstrates, celebrates, criticizes, or leaves unresolved;
- degree of certainty and source basis;
- narrator or host position;
- relationship to participants and audience;
- ethical and cultural stance;
- counter-position and credible alternatives;
- protected ambiguities;
- tonal contract.

This is more precise than “tone of voice.” It determines what the camera, edit, narration, and sound are allowed to imply.

### 3.4 Audience Experience Model

This model tracks hypotheses about the viewer, never simulated certainty. It includes:

- entry state: knowledge, assumptions, emotion, trust, and context;
- desired exit state;
- evolving questions and expectations;
- information load and required orientation;
- emotional and energy curves;
- attention targets and intended eye/ear focus;
- tension, curiosity, relief, surprise, reflection, and memory anchors;
- trust gains and possible violations;
- target-audience screening evidence.

Automated models can flag likely confusion or redundancy. Only real audience evidence can validate how viewers actually respond.

### 3.5 Story and Argument Model

This is a typed dramaturgical graph, not an ordered list of paragraphs. It represents:

- premise, controlling question, stakes, and payoff;
- characters, forces, goals, obstacles, changes, and relationships where applicable;
- claims, evidence, counterclaims, demonstrations, and causal dependencies;
- setups, callbacks, reveals, reversals, contrasts, and resolutions;
- thematic motifs and transformations;
- alternative orders and omitted paths;
- factual versus interpretive versus metaphorical material;
- what each unit changes in the viewer model.

For documentary and interview-led work, this model can emerge from logged material rather than precede capture.

### 3.6 Direction Model

The Direction Model is the operational equivalent of a director’s treatment and visual/sonic concept. It defines:

- governing formal idea;
- point of view and distance from subject;
- scene and sequence modes;
- camera and staging principles;
- production-design and material world;
- color and lighting progression;
- performance principles;
- sound perspective and music concept;
- graphic and motion language;
- tempo, contrast, restraint, and escalation;
- signature moments worth disproportionate investment;
- anti-vision: clichés, techniques, references, and emotional effects to avoid.

The Direction Model must be proven through artifacts, not approved as persuasive prose alone.

### 3.7 World and Continuity Model

This maintains entities and their continuity across live-action, archive, design, and generation:

- people/characters, appearance, wardrobe, voice, state, relationships, and chronology;
- locations, spatial relationships, time, weather, practical light, and visual identity;
- objects, props, interfaces, data, and recurring symbols;
- production design, textures, palette, typography, graphic assets, and materials;
- continuity rules and intentional discontinuities;
- identity anchors and approved reference media for generation;
- rights, disclosure, and depiction constraints.

This model is essential for synthetic material, but it also prevents ordinary editorial continuity errors.

### 3.8 Performance Model

Performance is not confined to actors. Narration, interview answers, presenters, hands in a product demo, animated characters, typography, and camera movement all perform.

The model records objective, subtext, emotional state, energy, pace, emphasis, gesture, reaction, breath, pronunciation, relationship, acceptable variation, takes, and selected moments. A “premium AI voice” with no performance direction remains generic.

### 3.9 Visual Language Model

This is a rule system with purpose and variation:

- framing and aspect logic;
- shot scale and lens/perspective behavior;
- camera height, movement, stability, and focus;
- staging, blocking, depth, eye lines, and screen direction;
- composition, hierarchy, value, contrast, and negative space;
- lighting source, quality, direction, contrast, and progression;
- color script and palette behavior;
- texture, image source, grain, sharpness, and materiality;
- visual motifs, recurrence, transformation, and retirement;
- transition principles;
- conditions under which rules may be broken.

Pixar’s film-grammar material explicitly treats framing, staging, camera movement, and editing as contributors to story, while its color-script material describes color and light as a way to map the film’s emotional arc. Disney Animation describes layout as a central storytelling process combining staging, cinematography, composition, rough performance, and editing. These are precisely the intermediate craft layers absent from clip assembly.

### 3.10 Sound World Model

This defines:

- subjective or objective listening perspective;
- dialogue and narration relationship;
- room tone, ambience, environmental identity, and off-screen space;
- recurring sonic motifs;
- effects realism versus expression;
- silence and dynamic range strategy;
- music’s dramatic function, structure, entrances, exits, and transformations;
- transitions led by sound, picture, or both;
- voice casting and performance;
- delivery format and accessibility.

Sound enters during direction and previs. It is not a bed selected after picture assembly.

### 3.11 Graphic and Motion System

This is not a template library. It defines:

- information hierarchy and reading order;
- typography roles and behavior;
- grid, spacing, scale, composition, and responsive rules;
- shape, line, icon, image, chart, map, and interface vocabulary;
- motion principles: cause, anticipation, acceleration, weight, continuity, transition, and rest;
- relationship to footage, camera, sound, and editorial rhythm;
- data truth and labeling requirements;
- component variants and controlled exceptions;
- what must be custom-designed.

Motion design practice typically moves through idea, moodboard, storyboard, style frames, and animatic before final animation. The animatic is where timing and pacing failures are discovered cheaply. The OS must encode that progression rather than jumping from text to executable animation code.

### 3.12 Production Value Map

Premium work does not spend uniformly. The map labels:

- signature/anchor moments that define the piece;
- narrative turns and proof moments that must be unmistakable;
- connective material that should remain simple;
- breaths and intentional low-density sections;
- reusable system elements;
- high-risk elements requiring prototypes;
- where human craft, commissioned work, or expensive generation has the highest value.

This prevents the system from applying equal synthetic effort to every sentence and allows a limited budget to create memorable authorship.

## 4. The Studio Brain

### 4.1 Why an agent chain is the wrong brain

A chain such as strategist → writer → director → producer → editor embeds three failures:

- it assumes the correct problem order before the work is understood;
- each role receives a lossy prose handoff rather than operating on shared evolving artifacts;
- the last agent’s locally plausible answer can overwrite unresolved upstream uncertainty.

The Studio Brain should use a **hierarchical blackboard architecture**. Blackboard systems were developed for problems where heterogeneous knowledge sources contribute opportunistically to a shared evolving solution and a control component decides what to activate next. Creative production has exactly that shape: the solution path is not fully known, evidence arrives over time, and story, direction, production, editorial, sound, and rights can each expose problems that reframe the others.

### 4.2 The Creative Blackboard

The blackboard is the working view of the Living Film Model. It contains, at every resolution:

- current committed decisions;
- candidate alternatives;
- constraints and preferences;
- evidence and material observations;
- conflicts and critique findings;
- open questions;
- dependencies and invalidations;
- confidence and provenance;
- cheapest available proof;
- current edit/prototype branches;
- readiness and production state.

Specialists do not chat with each other. They read a scoped blackboard view and submit typed proposals, patches, findings, questions, or work orders.

### 4.3 The Deliberation Controller

The controller chooses the next useful action. It does not ask, “Which department comes next?” It asks:

1. What high-impact decision or uncertainty currently limits the work?
2. What is its cost of remaining unresolved?
3. How reversible is the downstream commitment?
4. What is the cheapest reliable artifact or experiment that could reduce the uncertainty?
5. Which human, model, tool, or craft surface is qualified to produce that proof?
6. What evidence or review will make the result sufficient to commit?

A useful priority heuristic is proportional to:

> creative impact × uncertainty × downstream irreversibility × cost of delay, divided by cost of the next proof

This is a scheduling heuristic, not an automatic taste equation. It ensures the system tests the dangerous assumptions before polishing low-impact details.

### 4.4 The deliberation cycle

Every significant creative problem moves through a dynamic loop:

1. **Sense:** gather commission, evidence, references, materials, constraints, and current state.
2. **Frame:** state the actual creative problem and what a successful resolution changes.
3. **Diverge:** create structurally different routes or repairs.
4. **Externalize:** turn the best routes into the lowest-cost useful proof—cards, sketches, style frames, sound sketch, storyboard, animatic, blocking study, paper edit, or cut branch.
5. **Experience:** play, inspect, compare, or screen the proof in time rather than judging its description.
6. **Critique:** identify observed failures and probable causes across relevant crafts.
7. **Decide:** select, reject, combine, defer, or request a new probe with explicit rationale.
8. **Commit:** lock only the decision scope justified by the proof.
9. **Propagate:** update dependent models, production plans, and tasks.
10. **Reopen:** when new material or an edit invalidates an assumption, deliberately return to the necessary level.

This loop operates at piece, sequence, scene, shot, and finishing levels. It is not a single pre-production phase.

### 4.5 Knowledge sources

Knowledge sources are bounded reasoning and craft modules, not permanent autonomous personalities:

- editorial strategy and audience research;
- research, evidence, and claim reasoning;
- dramaturgy and argument design;
- directing and scene construction;
- performance and voice direction;
- cinematography, blocking, and visual continuity;
- production design and visual development;
- documentary logging and paper-edit reasoning;
- editing, montage, continuity, and rhythm;
- sound direction, music, dialogue, and mix planning;
- graphic design, information design, and motion direction;
- production topology, scheduling, budget, and feasibility;
- asset, rights, likeness, and provenance;
- NLE/DCC execution and rendering;
- screening analysis, craft critique, and technical QC;
- platform packaging and release;
- performance analysis and studio memory.

A single capable model may implement several knowledge sources. A separate worker is justified only by different context, tools, permissions, evaluation, cost, or failure isolation.

### 4.6 Hard constraints, soft constraints, and hypotheses

The brain must distinguish:

- **Hard constraints:** rights, budget ceilings, required claims, delivery specifications, deadlines, prohibited depictions, approved identities.
- **Soft constraints:** preferences such as restraint, pace, camera behavior, texture, or degree of humor.
- **Creative hypotheses:** beliefs that a structure, image, performance, sound idea, or package will cause an audience effect.
- **Evidence:** source facts, material observations, screening responses, analytics, and technical measurements.

An LLM must not convert a preference into a hard rule or a hypothesis into a fact. Creative hypotheses should be tested through prototypes and screenings.

### 4.7 The Taste and Judgment Model

A brand guide and an embedding of reference videos are not taste. The model is learned through **contextual preference evidence**:

- pairwise comparisons between references, treatments, boards, takes, cuts, and packages;
- the user’s reason for preferring one;
- what dimension mattered: point of view, restraint, tension, performance, composition, rhythm, texture, sound, humor, or another quality;
- the context and format where the preference applies;
- negative examples and local clichés;
- exceptions where breaking a prior preference succeeded;
- confidence and ratifying owner.

The system deconstructs references into mechanisms and asks for correction. It does not learn “make it look like creator X.” Pairwise judgments are useful because comparative taste is easier to articulate than absolute scoring, but research also shows LLM evaluators can diverge from human preferences and exhibit position, length, and shortcut biases. Human-calibrated preference evidence remains authoritative.

### 4.8 Memory writing

The brain has separate memories:

- **Studio memory:** constitution, audience promise, values, long-lived taste, autonomy, and risk.
- **Format memory:** craft protocol, successful mechanisms, failure patterns, reusable systems, and production benchmarks.
- **Production memory:** exact decisions, artifacts, material, edit branches, reviews, and release.
- **Capability memory:** provider/tool performance by task, cost, failure mode, and rights behavior.
- **Learning proposals:** observations awaiting corroboration and ratification.

Raw model output, one successful video, or one retention graph never automatically becomes lasting creative law.

## 5. The real editorial stack: the Audiovisual Score

### 5.1 The timeline is an execution projection

A professional NLE timeline represents media and operations over time. It does not itself contain all dramatic, perceptual, directorial, and production reasoning. The OS therefore needs an **Audiovisual Score** above the NLE timeline.

The score is analogous to a film plan, musical score, scene map, edit decision structure, and production graph combined. It preserves hierarchy and cross-craft relationships while allowing frame-accurate bindings once material exists.

### 5.2 Score hierarchy

Each piece contains movements/acts, sequences, scenes/segments, beats, shots/events, and elements. Every unit may specify:

- dramatic or explanatory job;
- viewer entry and intended exit state;
- question, objective, obstacle, turn, reveal, or information delta;
- point of view and subject relationship;
- duration hypothesis and elasticity;
- dominant formal mode;
- transition in and out;
- production-value class;
- required proof and material;
- current branch and maturity;
- upstream/downstream dependencies.

### 5.3 Coordinated score lanes

The score contains linked lanes rather than only video/audio tracks.

#### Dramaturgy lane

Questions, goals, conflict, claims, evidence, information changes, reveals, callbacks, power shifts, emotional turns, and payoffs.

#### Audience lane

Orientation, attention target, knowledge, uncertainty, tension, emotion, trust, energy, cognitive load, and intended memory anchors. These remain hypotheses until screened.

#### Performance lane

Speaker/character objective, line or action, subtext, delivery, gesture, reaction, breath, take options, and chosen performance moments.

#### Visual/staging lane

Location/world, subject placement, blocking, spatial relationships, props, shot design, frame, lens/perspective, movement, focus, light, color, texture, eye trace, and continuity.

#### Editorial lane

Shot order, selection, duration, montage function, cut motivation, overlap, ellipsis, reaction, match, discontinuity, visual rhythm, and branch alternatives.

#### Sound lane

Dialogue, narration, ambience, effects, music, silence, perspective, spatial field, dynamic state, transitions, and mix intent.

#### Graphics/motion lane

Information function, content truth, composition, hierarchy, typography, diagram/chart state, animation behavior, relationship to camera and sound, and readability.

#### Production lane

Designed requirement, source/take/candidate bindings, handles, version, rights, cost, status, VFX/motion task, DCC host, and fallback.

#### Finishing/variant lane

Color intent, VFX, cleanup, caption/audio-description requirements, crop/reframe behavior, localization, platform variants, and master state.

### 5.4 Scene Design

A Scene Design is not “show a hallway for five seconds.” It includes:

- scene job and why it must exist;
- event and change;
- point of view;
- entry/exit viewer state;
- character/speaker objectives and performance beats;
- space, time, blocking, and meaningful objects;
- visual strategy and shot grammar;
- sound perspective and musical behavior;
- graphic/information role;
- tempo and duration range;
- transition from previous and into next scene;
- required coverage and editorial options;
- non-negotiable moment;
- risks and cheapest proof.

Blocking is explicitly the construction of subject/object and camera positions in anticipation of editing. Standard generic coverage produces generic scenes. The system should first design how staging and camera express subtext, power, orientation, or discovery, then determine necessary coverage.

### 5.5 Shot Intent

A Shot Intent is independent of the media file that may fulfill it. It specifies:

- what the shot lets the viewer perceive now;
- focal subject and attention path;
- dramatic, evidential, spatial, emotional, or rhythmic function;
- point of view and emotional distance;
- composition, scale, angle, lens/perspective, camera height, and movement;
- subject blocking/action and performance beat;
- light, color, texture, depth, and continuity;
- sound relationship;
- desired start/end state and cut handles;
- duration elasticity;
- acceptable substitutions and prohibited clichés;
- live-action, archive, animation, graphic, synthetic, or hybrid realization routes.

Only after a Shot Intent exists should the system retrieve, commission, capture, design, or generate a candidate. A clip is a possible realization, not the shot.

### 5.6 Cut Decision

A cut is a relation between outgoing and incoming audiovisual states. Its record includes:

- why the cut occurs now: emotion, story, rhythm, eye trace, performance, reveal, continuity, or deliberate rupture;
- what information or power changes;
- outgoing and incoming attention targets;
- motion, composition, color, shape, gaze, and spatial relationships;
- audio lead, overlap, interruption, or silence;
- continuity preserved or intentionally broken;
- expected effect of holding longer or cutting earlier;
- selected branch and alternatives.

This is the actual editorial reasoning absent from “clip X, in A, out B, fade.”

### 5.7 Sequence Design

A sequence is a sustained movement, not a folder of scenes. It defines:

- beginning condition and ending transformation;
- internal escalation or progression;
- dominant formal mode and permitted departures;
- visual and sonic motif development;
- variation and repetition strategy;
- information and emotional density;
- signature image/sound and production-value allocation;
- transition architecture;
- runtime range and removable modules;
- how it changes the total piece.

This is especially important for faceless video. Instead of assigning a new random visual to every line, a 30–90 second sequence can inhabit one designed visual world, mechanism, or documentary situation and develop within it.

### 5.8 Time is progressive, not prematurely exact

Before performance and material exist, use duration ranges, relative order, synchronization targets, and elastic beats. Storyboards and animatics resolve provisional time. Actual takes and edit branches resolve record time. Picture lock resolves frame time; final audio resolves sample time.

Freezing exact seconds during script planning creates brittle animation and forces narration to serve a precomputed timeline.

### 5.9 Branches and editorial hypotheses

The score must support alternative scene orders, performances, openings, visual strategies, music approaches, and cut versions. An edit branch is a hypothesis about how the work plays. It is compared through screening and craft critique, then merged or rejected with reasons.

The system should never present one AI assembly as if it were the inevitable cut.

### 5.10 NLE projection and round trip

The Audiovisual Score compiles a branch into:

- a native OS proxy timeline for screening;
- an OpenTimelineIO interchange projection;
- Premiere, Resolve, or other host operations through adapters;
- VFX, motion, sound, and color turnovers;
- a final render graph when the OS owns execution.

Stable semantic IDs travel as markers, metadata, clip names, sidecars, or plugin-managed mappings. Changes made in the NLE return as structured diffs: trims, moves, replacements, effects, markers, audio changes, and new media. The OS asks for intent when a change cannot be inferred; it does not overwrite professional editorial work with a regenerated timeline.

## 6. Craft Protocols: there is no universal production flow

A Craft Protocol defines required artifacts, deliberation triggers, production topology, craft capabilities, review modes, and completion conditions for a class of work. The Studio Brain selects and composes protocols after framing the commission.

### 6.1 Documentary and faceless editorial essay

The correct flow may be:

- question, thesis, access, and evidence plan;
- source research, archive, interview or narration strategy;
- material logging, transcript ranges, quote/evidence graph, and selects;
- story cards or paper edit;
- argument/character structure and sequence map;
- director’s treatment and visual/sound concept;
- archive, actuality, reconstruction, graphics, and designed-sequence plan;
- radio cut or narrative assembly;
- style frames, scene boards, and animatic for designed sequences;
- rough cut with active coverage gaps;
- archive/graphics/sound production in context;
- screenings, restructuring, fine cut, and finish.

Documentary editors often discover structure by logging, grouping, and arranging real material; transcript-based paper edits identify meaningful statements, tone, conflict, and relationships. Forcing an approved script before editorial discovery would damage this format.

For faceless work, the protocol must prohibit sentence-level B-roll mapping. Each sequence chooses a dominant mode: archival investigation, designed spatial metaphor, diagrammatic explanation, screen evidence, character-focused actuality, essayistic montage, or another coherent form.

### 6.2 Interview, podcast, and expert-led work

The flow emphasizes:

- editorial objective and guest/subject model;
- interview architecture and follow-up logic;
- set, camera, lens, blocking, lighting, wardrobe, and sound design;
- performance safety and authenticity;
- multicamera/isolated-audio capture;
- sync, transcript, semantic logging, reactions, pauses, and selects;
- paper edit or radio cut;
- story construction from actual performance;
- contextual evidence, archive, graphics, and pickup requirements;
- picture edit, sound, color, and derivatives.

The system must preserve performance and conversation dynamics rather than over-compressing speech into optimized information.

### 6.3 Motion design and animated explainer

The flow is:

- problem, concept, audience, and information architecture;
- competing formal concepts;
- moodboards with mechanism annotations;
- rough boards and transition ideas;
- style-frame routes and design-system tests;
- color and type behavior;
- sound concept and voice performance;
- full storyboard/design boards;
- animatic with temp sound and voice;
- timing, comprehension, transition, and production review;
- asset design and production boards;
- animation by scene/shot;
- compositing, sound design, color, and finish.

Animation begins only after composition and timing are credible. LLM-generated HTML or motion code is an execution candidate for a designed board, never a substitute for boards and animatics.

### 6.4 Captured live-action narrative or brand film

The flow is:

- concept, treatment, screenplay or scenario;
- casting and performance concept;
- visual development and production design;
- location/scouting and practical constraints;
- scene breakdowns, blocking, storyboards, shot design, and coverage;
- rehearsals, camera/lighting/sound tests, and previs where needed;
- schedule and production plan;
- capture with script supervision and metadata;
- dailies, selects, continuity, and pickup detection;
- assembly, director/editor rough cut, screenings, fine cut;
- ADR, VFX, sound, music, color, online, and mastering.

The shot list is a production projection of scene and camera reasoning, not the creative source of truth.

### 6.5 Product, screen, and interface film

The flow is:

- product truth, target user job, and prohibited exaggerations;
- demonstration thesis and interaction story;
- real UI/data state and reproducible capture environment;
- choreography of pointer, touch, state changes, camera, and voice;
- boards and animatic;
- screen capture, macro product photography, 3D/product renders, or live action;
- graphics that clarify without falsifying behavior;
- edit, sound, legibility, accessibility, and platform variants.

The product action—not abstract shapes—must remain the source of visual causality.

### 6.6 Synthetic, 3D, and virtual production

The flow requires more control, not fewer steps:

- world/character/asset continuity package;
- concept art, look development, environment, materials, and lighting tests;
- storyboard and camera layout;
- identity and motion anchors;
- animatic or real-time previs;
- shot-by-shot generation or 3D execution with continuity constraints;
- dailies evaluation against shot intent;
- repair, compositing, cleanup, sound, edit, color, and disclosure.

Current long-form video generation still struggles with identity and scene consistency over multiple shots. Therefore synthetic output must be evaluated as takes, not treated as finished scenes.

### 6.7 Hybrid composition

Most premium online work is hybrid. The protocol composes subprotocols per sequence: documentary archive, bespoke motion graphics, interface demonstration, live presenter, 3D reconstruction, and sound-led montage may coexist. The Direction Model and Audiovisual Score maintain coherence across them.

Hybrid does not mean random. Each transition between production modes must have a narrative and formal reason.

## 7. The end-to-end operating flow

The flow is not a one-way pipeline. It is a sequence of progressively more expensive commitments connected by deliberation loops.

### 7.1 Studio calibration

The user does not begin by filling brand-color fields. The OS conducts a creative calibration:

- collect previous work, admired and rejected references, audience context, constraints, skills, tools, budget, and ambition;
- deconstruct references into story, framing, staging, design, sound, rhythm, performance, and finish mechanisms;
- run pairwise choices that force useful trade-offs: clarity versus mystery, polish versus immediacy, density versus space, narrator authority versus discovery, graphic abstraction versus material reality;
- establish a negative canon of clichés and misrepresentations;
- define autonomy and decisions the user wants to retain;
- determine actual available production topologies and capability quality.

The output is a provisional Studio Constitution and Taste Model. Both evolve only through ratified evidence.

### 7.2 Commission and creative diagnosis

Inputs may be an idea, brief, script, article, research dossier, product, footage, campaign objective, or existing cut. The brain diagnoses what actually exists and what is missing.

A script is never assumed to be good or even necessary. The brain may conclude that the project needs more access, a stronger thesis, better evidence, a different format, a smaller scope, or a human director before production should begin.

The output is the Creative Problem Model, risk/uncertainty ledger, candidate Craft Protocols, and a plan for the next cheapest evidence.

### 7.3 Research, access, and point of view

The system builds factual evidence, audience/cultural context, source material, participant access, competitor/reference analysis, and the editorial point of view. It distinguishes:

- what is known;
- what is claimed;
- what can be shown;
- what can only be told;
- what is uncertain;
- what is ethically or legally inappropriate;
- what the creator can uniquely contribute.

The output is not a generic research summary. It is a set of story and form opportunities grounded in usable material.

### 7.4 The Route Room

The brain produces a small set of **Creative Routes** that are structurally different. Each route contains:

- thesis and audience promise;
- narrator/host/subject relationship;
- story or argument engine;
- formal device and production topology;
- representative scene or sequence;
- visual, sound, performance, and graphic principles;
- signature moment;
- risks, cost, rights, and capability needs;
- anti-vision;
- cheapest decisive prototype.

The user selects a direction by comparing routes, not by approving a long document. If the difference cannot be felt, the alternatives are not meaningfully different.

### 7.5 Direction development

The selected route becomes a Direction Model, experience arc, story/argument model, production-value map, and preliminary sequence map. The brain identifies the governing craft questions and commissions proofs:

- style frames for appearance and composition;
- a color script for progression;
- a sound sketch for perspective and tone;
- a voice/performance test;
- scene boards for staging and visual grammar;
- a paper edit or radio fragment for argument and performance;
- a motion study for animation behavior;
- a blocking/previs study for complex scene action;
- a synthetic continuity test for generated characters/worlds.

Direction is greenlit only when the high-impact premise is demonstrated in time or image/sound—not merely described.

### 7.6 Previsualization and the first complete experience

The OS creates the lowest-fidelity complete version appropriate to the Craft Protocol:

- boardomatic or story reel;
- animatic;
- radio cut with boards;
- documentary paper edit plus representative visual sequences;
- real-time previs;
- product interaction animatic;
- rough scene assembly.

This version is screened end to end. It exposes missing orientation, weak progression, tonal inconsistency, repetitive visual modes, false pace, expensive scenes that add little, and transitions that exist only on paper.

The output is a validated or revised Audiovisual Score, scene/shot designs, sound plan, and production plan.

### 7.7 Production design and planning

The producer converts the approved score into execution while protecting its creative intent:

- break down scenes, shots, graphics, sound, performances, assets, VFX, and variants;
- decide capture, commission, license, design, animate, generate, reuse, or external DCC execution;
- group work by setup, location, artist, environment, model, tool, or renderer;
- allocate budget according to the Production Value Map;
- create schedules, dependencies, rights requirements, review owners, and fallbacks;
- verify that every work order has a useful creative and technical acceptance test.

Hard scheduling and allocation problems should use constraint solving. A language model may propose options, but it should not pretend arithmetic and resource constraints are creative prose.

### 7.8 Production and dailies

Every delivery is treated as a take or candidate against a designed intent:

- ingest originals with identity, timecode, technical metadata, source, rights, and continuity context;
- create proxies, transcripts, waveforms, thumbnails, contact sheets, and technical analysis;
- compare candidates with Shot Intent, Performance Model, world continuity, visual language, and required handles;
- record selects, alternates, partial successes, rejection reasons, and pickup/repair needs;
- update the score when material reveals a better creative route;
- prevent unqualified material from silently becoming “available media.”

Dailies are a creative feedback system. A beautiful shot that does not cut, breaks continuity, or violates the scene is not successful material.

### 7.9 Editorial discovery and construction

The editor works with the footage, sound, graphics, and score rather than mechanically realizing a locked plan. The passes depend on format, but the complete stack includes:

1. **Logging/selects:** understand material, performance, evidence, mistakes, surprises, and latent connections.
2. **Paper/radio/story edit:** make meaning, argument, character, performance, and orientation work without decorative visual rescue.
3. **Scene construction:** find the internal event, point of view, reactions, spatial logic, duration, and sound behavior.
4. **Sequence construction:** build progression, escalation, formal continuity, motif development, and transitions.
5. **Assembly:** test the complete work and reveal structural failures.
6. **Rough-cut exploration:** create branches, reorder, remove, rebuild, and find the actual film rather than protect the plan.
7. **Screening:** observe comprehension, emotion, trust, energy, and attention; separate symptom from cause.
8. **Fine cut:** refine performance, shot choice, frames, J/L cuts, eye trace, breath, emphasis, and redundancy.
9. **Structure/picture lock:** lock only after production dependencies and expected creative gain justify it.

Frame.io’s professional workflow guide notes that an assembly can be far from the finished film and that director/editor rough-cut work may rebuild scenes from scratch. The architecture must preserve that freedom rather than treating editing as execution of pre-production instructions.

### 7.10 Post-production and finishing

Post is a coordinated set of crafts:

- VFX turnover, tracking, cleanup, compositing, and final graphics;
- dialogue edit, ADR where needed, sound effects, ambience, Foley, music edit/score, premix, and final mix;
- conform to original media and verify every shot/version;
- color management, grade, look continuity, and delivery transforms;
- titles, captions, audio description, localization, credits, and disclosures;
- online QC, master, and derivative builds.

Sound and graphics may continue to reshape picture before lock. Finishing is not one renderer job.

### 7.11 Release and learning

Packaging is treated as the final expression of the work’s actual promise. Private staging, platform checks, rights, disclosures, captions, metadata, approvals, and publication receipts remain mandatory.

After release, the system compares observed outcomes with the pre-release hypotheses and qualitative audience response. It proposes scoped lessons with confounders. It does not optimize every future opening toward the latest retention curve.

## 8. Anti-slop invariants

These are enforced product rules, not style suggestions.

### 8.1 No sentence-to-clip mapping

Narration sentences may link to beats and evidence, but they never directly trigger one stock search or generation job each. Visual planning occurs at scene, sequence, and shot-intent levels.

### 8.2 No media without a designed role

Every used asset, generated shot, graphic, sound cue, text element, and transition must bind to a Shot Intent, Scene Design, Cut Decision, Sound Intent, or Graphic Intent. “It looks good” is insufficient.

### 8.3 No sequence without a formal idea

Every substantial sequence declares a dominant visual/sonic mode, progression, signature moment, and transition logic. Randomly alternating archive, AI imagery, charts, and kinetic text is a violation.

### 8.4 No final production before proof

High-risk direction must be tested with a proportionate low-cost proof. Motion design requires boards/style frames/animatic; complex live action requires blocking or previs; long synthetic scenes require continuity tests; sound-led concepts require sound sketches.

### 8.5 No universal “engagement pacing”

The system cannot prescribe constant motion, cuts every N seconds, background music everywhere, or hooks divorced from the work. It analyzes progression and contrast at multiple timescales.

### 8.6 No duplicate channels by default

If narration, text, image, and sound communicate the same information, the brain must justify the reinforcement or remove redundancy. Each channel should extend, prove, contrast, locate, embody, or transform.

### 8.7 No animation before design

Typography, information hierarchy, composition, spacing, and visual logic must work in representative still frames before animation. Motion cannot rescue weak design.

### 8.8 No generic B-roll as a silent substitution

If no candidate meets the specificity threshold, the system returns a creative gap. It may propose a graphic explanation, new capture, archive research, reconstruction, rewrite, omission, or explicit compromise. It may not quietly use topic-adjacent footage.

### 8.9 No single-candidate acceptance for signature moments

Anchor moments require deliberate alternatives or a documented reason why only one feasible path exists. The system presents contact sheets, auditions, board variants, or cut branches in context.

### 8.10 No generated continuity by prompt memory alone

Recurring people, locations, objects, interfaces, camera rules, light, sound, and design use explicit continuity packages and reference anchors. Every synthetic delivery is checked for identity, world, motion, and semantic drift.

### 8.11 No music as emotional wallpaper

Music must have a dramatic job, structural entry/exit, relationship to dialogue and effects, and rights status. Continuous generic beds are flagged unless the format deliberately requires them.

### 8.12 No review by global score

Review produces time/artifact-specific observations, probable causes, violated intentions or craft rules, severity, and alternatives. A global AI quality score cannot greenlight work.

### 8.13 The system may refuse to finish

If thesis, evidence, direction, material, performance, or execution quality cannot meet the approved floor, the correct result is a blocker, revised scope, or request for human craft—not a complete slop video.

## 9. Human interfaces

These are decision and collaboration protocols, independent of UI layout.

### 9.1 Commissioning interface

The user may supply incomplete natural language and files. The system returns a structured diagnosis: understood objective, assumptions, contradictions, missing access/evidence, candidate production topology, risk, and next decision. It does not immediately generate a script.

### 9.2 Taste calibration interface

The system presents pairwise references or internal variants with one focused question at a time. The user selects and explains. The output is contextual Preference Evidence, not a hidden prompt update.

### 9.3 Route decision interface

Each route is presented through comparable treatment, representative scene, style/sound proof, cost, risk, and production consequences. The user can select, combine specific mechanisms, request a probe, or reject the commission.

### 9.4 Direction review interface

The user reviews time-based and visual proofs: boards, style frames, color script, voice test, sound sketch, animatic, or previs. Feedback must identify the experienced effect—“too polished to feel forensic,” “I understand the claim before I feel the trap”—rather than only prescribing surface changes.

### 9.5 Dailies interface

The director/editor sees candidate material synchronized with Shot Intent and continuity references. They select, circle, reject, request pickups, or revise the plan. Selection reasons are retained.

### 9.6 Screening interface

A screening is tied to an immutable cut/prototype version. Reviewers can mark confusion, emotion, attention, trust, rhythm, performance, sound, and craft. Feedback is separated from proposed repair. Contradictory findings become a decision, not averaged sentiment.

### 9.7 Craft handoff interface

Artists receive a self-contained work package: scene/shot intent, context excerpt, source media, references with mechanism notes, technical spec, handles, color/sound context, rights, output contract, and review owner. They return editable sources, rendered outputs, versions, and a publish receipt.

### 9.8 Exception interface

When budget, rights, material, time, or capability forces compromise, the system presents options with creative consequences. The producer cannot silently replace the shot; the creative owner cannot approve an impossible idea without accepting cost/schedule change.

## 10. System contracts

All contracts are schema-versioned, artifact-addressed, and carry production scope, author/worker identity, parent versions, provenance, state, and validation.

### 10.1 Creative Problem

Contains audience, objective, thesis candidate, deliverables, context, constraints, access, evidence state, capabilities, risk, unknowns, failure definition, autonomy, and decision owners.

### 10.2 Creative Route

Contains editorial point of view, audience promise, story engine, formal concept, production topology, representative sequence, visual/sound/performance principles, signature moments, anti-vision, feasibility, risks, and proposed proof.

### 10.3 Blackboard Contribution

Every specialist returns one of:

- proposal;
- artifact patch;
- critique finding;
- alternative set;
- open question;
- constraint conflict;
- experiment/proof request;
- work order;
- decision request;
- execution receipt.

It includes exact target artifacts, rationale, evidence, assumptions, confidence by claim, expected impact, and validation schema.

### 10.4 Open Question and Proof Request

An Open Question records uncertainty, affected decisions, impact, deadline, owner, and current evidence. A Proof Request identifies the cheapest artifact/experiment, capability, cost, acceptance test, and decision it will unlock.

### 10.5 Sequence Design

Contains transformation, internal progression, formal mode, motif behavior, scene membership, audience and rhythm hypotheses, production-value allocation, transitions, runtime elasticity, dependencies, and signature moment.

### 10.6 Scene Design

Contains event/change, point of view, performance objectives, blocking/space, camera/visual strategy, sound perspective, graphics, tempo, transitions, coverage, risk, and proof.

### 10.7 Shot Intent

Contains perceptual function, attention target, dramatic/evidential role, point of view, staging, camera, performance, light/color/texture, sound relation, continuity, duration/handles, substitutions, and realization routes.

### 10.8 Sound Intent

Contains narrative function, source/world relation, listener perspective, spectral/spatial/dynamic behavior, timing elasticity, dialogue/music/effects interactions, motif, transition, and deliverable requirements.

### 10.9 Graphic/Motion Intent

Contains information job, source truth, reading order, composition, typography, design-system bindings, animation cause/behavior, sound/camera relationship, duration, responsiveness, and accessibility.

### 10.10 Work Order

Contains target intent, source context, references and mechanism notes, required/optional/prohibited properties, continuity anchors, technical spec, editable-source requirement, rights/security, candidate strategy, budget, deadline, acceptance tests, reviewer, and fallback.

A prompt is a provider-specific implementation detail inside a work order.

### 10.11 Candidate/Take Delivery

Contains source/editable file, preview, identity, timecode/range, provider/artist, parameters, cost, provenance, rights, technical analysis, continuity analysis, intent-fit findings, handles, limitations, and worker notes. Delivery does not imply selection.

### 10.12 Audiovisual Score and Edit Branch

The score contains hierarchy, coordinated lanes, time hypotheses, semantic relations, intent bindings, production status, variants, and craft ownership. An Edit Branch pins a score version, media bindings, NLE/native projection, editorial decisions, unresolved gaps, and screening history.

### 10.13 NLE/DCC Change Set

Contains host/project/sequence identity, semantic mapping, operations performed, source and result versions, trims, placements, replacements, effects, markers, media publications, conflicts, and human intent notes. It enables round trip without assuming every host feature maps losslessly.

### 10.14 Critique Finding

Contains observed effect/problem, target version and range, review lens, linked intention or craft rule, evidence, severity, probable cause with uncertainty, possible repairs, owner, disposition, and verification.

### 10.15 Preference Evidence

Contains alternatives, selected option, dimension, reason, context, scope, strength, exception conditions, owner, and confidence. It updates the Taste Model only after policy-defined ratification.

### 10.16 Execution Bundle and Publish Receipt

The bundle contains exact source identities, editable workfile or render graph, tool/plugin/font/color dependencies, versions, handles, outputs, and acceptance tests. The receipt records outputs, checksums, environment, logs, warnings, validation, and newly published asset references.

## 11. Component architecture

The boundaries below are logical ownership domains. The initial deployment should not turn each bullet into a microservice.

### 11.1 Studio Brain Plane

#### Creative Blackboard Service

Maintains current problem-solving views over the Living Film Model, alternatives, questions, conflicts, findings, and readiness. It does not replace the underlying artifact/version store.

#### Deliberation Controller

Prioritizes open problems, chooses proof type, activates knowledge sources, enforces stop/commit conditions, and routes decisions. It owns control policy, not creative truth.

#### Context Compiler

Builds exact task context from approved artifact versions, relevant branch state, evidence, continuity, taste, constraints, capabilities, and negative rules. It explicitly lists omissions and untrusted inputs.

#### Constraint and Feasibility Engine

Evaluates hard constraints, detects conflicts, performs schedule/resource/budget optimization, and returns feasible options. Use graph algorithms and constraint solvers for deterministic problems.

#### Taste and Preference Service

Stores contextual pairwise evidence, reference deconstruction, negative canon, local exceptions, and calibration metrics. It never converts one choice into a universal style rule.

#### Decision and Authority Service

Owns approvals, delegated autonomy, risk policies, exceptions, decision scope, expiration, and accountable owners.

### 11.2 Living Film Plane

#### Artifact and Version Service

Owns immutable typed versions, branches, diffs, lineage, schema migration, approval scope, and locks.

#### Film Graph and Impact Service

Owns relations among thesis, evidence, sequences, scenes, shots, assets, rights, work orders, edits, reviews, and releases. It calculates staleness and bounded rework.

#### Story/Argument Service

Owns claims, evidence, characters/forces, dependencies, questions, turns, setups/payoffs, themes, and alternate structures.

#### Direction and Visual Development Service

Owns routes, treatments, visual/sound/performance systems, color scripts, reference mechanisms, style frames, boards, and proof artifacts.

#### Audiovisual Score Service

Owns the multi-resolution hierarchy, coordinated lanes, scene/shot/cut/sound/graphic intents, time hypotheses, variants, and edit branches.

#### World, Performance, and Continuity Service

Owns entities, identity anchors, state changes, space, props, wardrobe, interface/data state, voice, performance, and cross-shot continuity.

### 11.3 Production Plane

#### Craft Protocol Registry

Defines artifact dependency templates, triggers, required specialists, review gates, completion criteria, and execution topology by format.

#### Production Planner

Converts score/designs into breakdowns, schedules, budget allocation, setup grouping, staffing, dependencies, fallbacks, and turnovers.

#### Capability Registry and Broker

Describes human, vendor, model, DCC, renderer, capture, research, and analysis capabilities by craft, controls, quality envelope, known failures, cost, latency, rights, privacy, availability, and output contracts. It matches work orders to qualified routes.

#### Asset, Rights, and Provenance Manager

Owns stable asset/version identities, storage resolution, descriptive/technical metadata, license/releases, use intent, clearance, credits, transformations, and provenance. Adopt OpenAssetIO-style identity references so DCC hosts resolve an entity rather than depending on fragile file paths.

#### Ingest, Dailies, and Media Intelligence

Owns upload/capture validation, hashing, timecode, proxies, sync, transcripts, OCR, contact sheets, waveforms, shot/scene segmentation, technical measurements, continuity observations, selects, and pickup findings.

#### Workfile and Publish Manager

Tracks editable DCC/NLE workfiles, dependencies, versions, artist contexts, validations, publications, and review outputs. AYON demonstrates useful patterns here: host integrations, loaders, publishers, workfiles, and scene/version management.

### 11.4 Editorial and Review Plane

#### Native Prototype/Preview Engine

Plays boards, animatics, proxy edits, basic graphics, audio, captions, and annotations. Its purpose is low-cost deliberation and screening, not replacement of every finishing tool.

#### NLE/DCC Bridge

Projects score/edit branches into host tools, maps semantic IDs, packages media, receives change sets and publications, and detects lossy or conflicting round trips.

#### Screening and Review Service

Owns immutable screening versions, reviewer roles, audience studies, annotations, craft findings, contradictions, resolutions, and verification.

#### Editorial Analysis Service

Computes deterministic features and model-assisted observations: speech/shot density, repeated imagery, eye-trace discontinuity candidates, silence/music distribution, graphic readability, evidence coverage, continuity, synthetic drift, and motif use. It produces findings, not automatic edit authority.

### 11.5 Craft Runtime Plane

#### Editorial Runtime

Native proxy engine plus Premiere/Resolve/Avid/Final Cut adapters and OTIO interchange.

#### 2D Design and Motion Runtime

Typed composition/animation components for bounded automated work plus After Effects, Fusion, Blender, or other DCC packages for authored execution.

#### 3D and Virtual Production Runtime

Blender and Unreal/other engines for previs, layout, camera, animation, lighting, simulation, and high-quality image sequences.

#### Audio Runtime

Internal stem assembly and analysis plus Fairlight/Pro Tools/DAW turnover for dialogue, effects, Foley, music, spatial mix, and final delivery.

#### Conform, Color, and Master Runtime

Original-media conform, OpenColorIO-aware processing, Resolve/color-host integration, FFmpeg packaging, captions, variants, QC, and masters.

### 11.6 Release and Learning Plane

Owns platform packages, private staging, checks, approvals, publication, corrections/takedowns, analytics snapshots, qualitative feedback, studies, and ratified learning.

## 12. Trigger architecture

The Studio Brain is event-reactive but not event-driven chaos. Domain events wake the Deliberation Controller, which evaluates whether a creative action is actually required.

### 12.1 New commission

Triggers diagnosis, missing-context detection, Craft Protocol candidates, risk classification, and a commissioning decision. It does not trigger script generation.

### 12.2 New or changed evidence

Triggers claim/argument impact analysis and flags dependent narration, graphics, scenes, captions, packages, and released corrections. It does not regenerate the entire piece.

### 12.3 Creative route selected

Triggers proof planning, Direction Model drafting, and high-risk uncertainty scheduling. Full production waits for the relevant proofs.

### 12.4 Prototype delivered

Triggers technical validation, relevant craft critique, and contextual comparison. Signature prototypes require a human direction decision.

### 12.5 Direction or sequence changed

Triggers score, world/continuity, sound, production, budget, and rights impact analysis. Only invalidated work is reopened.

### 12.6 Work order ready

Triggers capability matching. Automatic execution is permitted only when authority, budget, rights, data policy, and quality evidence allow it.

### 12.7 Candidate/take delivered

Triggers ingest, technical analysis, continuity/intent-fit review, and dailies presentation. It never triggers automatic timeline insertion merely because generation succeeded.

### 12.8 Edit branch changed

Triggers lightweight dependency checks immediately and deeper story, rhythm, sound, continuity, graphics, rights, and screening evaluation at milestone conditions. Avoid running expensive full evaluators after every trim.

### 12.9 Human feedback submitted

Triggers classification into observation, preference, constraint, decision, question, or proposed repair. Ambiguous feedback is clarified before it becomes a persistent rule.

### 12.10 Blocker or capability failure

Triggers replan across alternate candidates, tools, capture, design, rewrite, scope, schedule, or budget. The broker cannot reduce the creative requirement without a decision.

### 12.11 Milestone candidate reached

Triggers the Craft Protocol’s gate: required artifacts, relevant screening, rights/evidence, production feasibility, technical checks, and named approval.

### 12.12 Release outcome available

Triggers a performance study and learning proposal, never an automatic constitution or format mutation.

## 13. Technology and tool stack

### 13.1 Architecture style

Start with a **modular monolith for domain/control logic**, separate durable-workflow infrastructure, object storage, PostgreSQL, and independently scalable media/AI workers. The creative model is already complex; microservices would multiply consistency problems before independent scaling or team ownership exists.

### 13.2 Core application

- Python with FastAPI and Pydantic for domain APIs, artifact schemas, media/AI integration, and rapid research tooling.
- SQLAlchemy and Alembic for explicit persistence and migrations.
- TypeScript/React for collaborative workbenches, boards, native prototype player, and review.
- JSON Schema for public artifact/capability contracts; OpenAPI for application APIs.
- JSON Patch or a typed patch DSL for blackboard contributions; never accept whole-document replacement from agents by default.

Python is appropriate because media, ML, optimization, pipeline, and DCC ecosystems are central. Critical timecode, graph, diff, and invariant code must be heavily tested; performance-critical media services can move to Rust/C++ only after profiling.

### 13.3 Durable workflow and control

- Temporal for production workflows, human waits, deadlines, retries, cancellations, compensation, and long-running external jobs. Temporal distinguishes deterministic workflow logic from external Activities such as LLM calls, API calls, and file operations, and supports durable human-in-the-loop waits.
- A custom Deliberation Controller above Temporal. Temporal provides reliable execution; it does not decide what is creatively useful.
- Do not use LangGraph, CrewAI, or another agent framework as the production source of truth. They may be used inside a bounded reasoning Activity if they prove useful, while Temporal and the domain store retain state.
- PostgreSQL transactional outbox for committed domain events; add NATS JetStream only when multiple real-time consumers justify it.

### 13.4 Data and memory

- PostgreSQL for operational truth, artifact/version metadata, typed relations, decisions, preferences, production state, reviews, and audit.
- JSONB for schema-versioned artifact bodies where structures vary by Craft Protocol, with important invariants promoted to relational columns/constraints.
- S3-compatible object storage for originals, proxies, editable sources, boards, audio, candidates, image sequences, work packages, renders, licenses, and receipts.
- PostgreSQL full text plus `pgvector` initially for semantic retrieval. Embeddings retrieve candidates; they never determine approval, rights, or current version.
- A derived graph database only if measured portfolio-scale traversals outgrow PostgreSQL recursive queries and materialized read models.
- Redis for cache, ephemeral progress, rate limits, and preview coordination only.

### 13.5 Planning and reasoning tools

- LLMs for framing, divergence, synthesis, narrative/argument proposals, critique candidates, and structured transformations.
- VLMs for board/frame/shot analysis, continuity candidates, composition observations, and reference deconstruction.
- audio/speech models for transcription, speaker separation, dialogue analysis, sound classification, and voice prototypes.
- deterministic graph algorithms for dependency and impact analysis.
- constraint programming such as OR-Tools CP-SAT for schedules, setup grouping, capability assignment, budget/resource constraints, and optimization.
- statistical or learned pairwise preference models only after sufficient human-calibrated project data exists.

No model is the “brain.” The brain is the deliberation architecture, authoritative artifacts, tools, evaluations, and human authority operating together.

### 13.6 Media ingest and analysis

- FFmpeg/ffprobe and PyAV for decode, probe, proxy, conform helpers, audio/video transforms, and encoding.
- OpenCV and specialist libraries for image/video measurements, tracking helpers, and quality features.
- ASR/diarization/OCR services with word/frame time alignment.
- scene and shot segmentation, duplicate/perceptual hashing, waveform/loudness analysis, black/silence/freeze detection, and metadata extraction.
- content hashes and immutable original preservation.

Automated annotations are observations with confidence and model version, not editorial truth.

### 13.7 Native preview/editor engine

Use a mature multitrack engine rather than building decode, seeking, mixing, and effects from scratch. MLT is a credible open-source candidate: it is designed to author and run multitrack audio/video compositions, is used by several NLEs, supports frame-accurate seeking, effects, OpenFX, vector animation formats, and hardware acceleration. It should be evaluated against licensing, color, audio, browser/client architecture, and required round-trip semantics before commitment.

The native engine’s first job is boards, animatics, proxy cuts, screening, annotations, and bounded automated sequences. It is not required to match a professional NLE’s complete editing and finishing feature set.

### 13.8 Editorial interchange and host integration

- OpenTimelineIO for cut-information interchange and media-linker/adaptor patterns, not as the Living Film Model.
- Premiere UXP as a strong first bidirectional NLE integration candidate. Its current API can access and modify projects, sequences, tracks, clips, markers, effects, playback, and export, allowing a persistent OS panel and commands inside the editing environment.
- Resolve/Fusion scripting and timeline/project interchange for editorial, color, audio, compositing, and final finishing; validate exact API and licensing capabilities against the chosen Resolve version.
- AAF/FCPXML/EDL where required as lossy interoperability formats, with explicit feature-loss reports.
- AYON or its architectural patterns for DCC host integration, workfiles, loaders, publishers, and asset/version context rather than inventing every pipeline mechanism.

The OS should choose one NLE bridge for the first Craft Protocol and make the round trip reliable before adding multiple shallow integrations.

### 13.9 Design, motion, VFX, and 3D

- A typed internal composition model for bounded automated text, charts, diagrams, maps, simple 2D motion, and branded components.
- Skia/Canvas/WebGL or an evaluated animation engine for real-time preview; render output must be deterministic and match approved typography/layout.
- After Effects/Premiere MOGRT, Fusion, or Blender adapters for authored 2D/2.5D motion and compositing.
- Blender Python/headless rendering for controlled 3D, animation, compositing, and image sequences.
- Unreal Sequencer and Movie Render Queue for real-time previs, virtual production, complex camera/scene work, and high-quality offline cinematic renders where its operational weight is justified.
- OpenFX where plugin licensing and host support allow.

Remotion, Motion Canvas, or arbitrary HTML are possible renderer implementations for narrow designed components. They are not the architecture and must never receive “script section → make something visually engaging” as an unconstrained contract.

### 13.10 Audio

- Native proxy mixing and stem management for editorial.
- Broadcast Wave/timecode-aware source handling where applicable.
- AAF/OTIO/host-specific turnover plus stems for Fairlight, Pro Tools, or another DAW.
- loudness, true-peak, phase, silence, sync, and channel-layout QC.
- music, voice, and SFX providers behind the same Work Order/Candidate/rights model as picture.

FFmpeg can measure and assemble audio. It is not a sound-design or final-mix methodology.

### 13.11 Color, master, and provenance

- OpenColorIO for explicit working/display/output color transforms across compatible tools.
- Resolve or another grading host for authored color where the project requires it.
- FFmpeg for deterministic packaging, codecs, variants, and selected QC.
- C2PA Content Credentials for supported provenance assertions and ingredient history; never treat provenance as proof of truth, ownership, or permission.
- immutable render/build manifests with source hashes, font/plugin/tool versions, color config, and output specs.

### 13.12 Observability and security

- OpenTelemetry across production, workflow, reasoning run, work order, asset, edit branch, and render IDs.
- tenant isolation, RBAC plus policy/attribute checks, scoped connector credentials, managed secrets, encryption, retention/deletion, and audit.
- treat web research, uploaded files, asset metadata, transcripts, comments, and model output as untrusted data, never instructions.
- sandbox generated code and DCC automation; deny network/file/publish permissions unless the work order explicitly grants them.
- cost, latency, cancellation, retry, and provider-quality telemetry per capability.

## 14. Concrete non-slop example

Consider a faceless video about scarcity manipulation. The old pipeline would narrate “only two left,” show an ecommerce page, add a countdown, cut to worried shoppers, and place tense music underneath.

The new system proceeds differently.

### 14.1 Route selection

Three routes might be tested:

- forensic interface investigation;
- invisible architecture that physically narrows choice;
- social experiment told through one character’s decisions.

The selected route is “invisible architecture.” The governing formal idea is that manipulation changes the viewer’s perceived space before they intellectually understand it.

### 14.2 Sequence design

The scarcity sequence begins in a visually open world and ends constrained. It has three escalating claims. The dominant mode is one continuous designed spatial metaphor, not three unrelated clips. The explanation is delayed until the viewer has felt the narrowing.

### 14.3 Visual development

Boards test corridor geometry, subject distance, available doors, camera behavior, value contrast, and the moment the environment stops feeling neutral. Style frames decide whether the world is photographic, graphic, or 3D. A color script shows warmth draining as choices disappear. A sound sketch progressively narrows stereo width, removes environmental detail, and introduces a pulse derived from the countdown rather than a generic tension track.

### 14.4 Animatic

The animatic uses boards, provisional camera moves, temp voice, and the sound sketch. Screening reveals whether the viewer feels pressure before the narration names scarcity. Timing is revised before 3D or generation begins.

### 14.5 Production

Shot Intents specify the spatial change, focal subject, camera distance, door positions, performance/reaction, light, sound relationship, cut handles, and continuity. Blender, a commissioned artist, or a controlled video model may realize them. Deliveries are takes checked against the common world and shot intent.

### 14.6 Editorial

The editor may hold a reaction longer, let a door close off-screen in sound, or remove an explanatory line because the designed scene now communicates it. The transition into price anchoring reuses the narrowing geometry as a visual match to manipulated scales, evolving the motif rather than changing to another template.

The result may still fail; no architecture can guarantee art. But it fails as a directed scene that can be diagnosed and revised, not as a polished pile of topical media.

## 15. Evaluation and validation

### 15.1 Evaluate the complete system, not generated assets

Metrics must cover:

- route distinctness and treatment acceptance;
- number and cost of uncertainties caught before production;
- prototype-to-final continuity of direction;
- Shot Intent fulfillment and candidate rejection/select reasons;
- structural edit rework after production;
- expert pairwise preference against baseline AI-video workflows;
- audience comprehension, emotion, trust, and memory relative to declared hypotheses;
- template/generic-material incidence;
- continuity, rights, evidence, accessibility, and technical escapes;
- creator recognition of authorship;
- time and cost by craft stage;
- how often the system correctly escalates rather than completes weak work.

### 15.2 Expert blind comparison

For each pilot, create:

- a conventional script-to-AI-video baseline;
- an OS-directed version using the same budget/capabilities;
- where possible, a human-led professional reference version.

Editors, directors, designers, sound practitioners, and target viewers compare versions blindly on specific dimensions and explain their preference. One model judge is not sufficient.

### 15.3 Golden production corpus

Retain approved and rejected routes, boards, style frames, animatics, takes, cut branches, sound sketches, review findings, rights failures, continuity errors, and final studies. Preserve the decision reason and context. This corpus becomes the basis for regression tests, retrieval, capability routing, and future preference models.

### 15.4 Failure suites

Test deliberately difficult cases:

- a polished but empty script;
- no usable visual access;
- conflicting brand references;
- strong footage that contradicts the planned story;
- low budget with one necessary signature moment;
- generative identity drift;
- bad performance with technically clean audio;
- graphics that repeat narration;
- misleading product depiction;
- late factual correction;
- an editor’s NLE changes that cannot round-trip losslessly;
- contradictory client and director notes;
- retention data suggesting the wrong creative cause.

The system is trustworthy only if it exposes these problems without defaulting to plausible completion.

## 16. Correct build order

### 16.1 Do not begin with the renderer

Building cloud rendering, asset generation, or a full standalone NLE first would encode the old assembly model again. The first proof must demonstrate better creative reasoning and editorial representation while professional humans and tools can execute the craft.

### 16.2 Vertical proof 1: one premium faceless-documentary protocol

Build:

- studio/taste calibration;
- Creative Problem and Route Room;
- research/claim and editorial point-of-view models;
- Direction Model;
- sequence/scene/shot intents;
- boards, style frames, sound sketch, and animatic workflow;
- Audiovisual Score;
- a manual/professional NLE execution bridge;
- screening, critique, and preference capture.

Use human designers/editors where necessary. The goal is to prove that the OS creates a more authored plan and cut than the baseline—not to prove maximum autonomy.

### 16.3 Vertical proof 2: dailies and NLE round trip

Add ingest, transcripts, selects, candidate/take qualification, continuity, work packages, Premiere or Resolve integration, semantic IDs, edit diffs, workfile publication, and rough-cut screenings. Prove that professional editorial changes remain first-class and do not get overwritten.

### 16.4 Vertical proof 3: bounded craft automation

Automate only well-specified tasks:

- research and evidence organization;
- transcript logging and paper-edit alternatives;
- board/style-frame candidate generation;
- simple typed graphics and diagrams;
- asset retrieval and candidate comparison;
- narration auditions;
- proxy assemblies from approved score branches;
- technical QC and impact analysis.

Measure quality and escalation behavior before automating signature scenes or final edit decisions.

### 16.5 Vertical proof 4: second, structurally different protocol

Add either interview/documentary discovery or full motion design. If the Living Film Model, brain, and score cannot support it without forcing the first protocol’s artifacts, the core abstractions are wrong.

### 16.6 Vertical proof 5: native preview and automated execution

Build the native multitrack/animatic/proxy runtime and typed 2D motion components. Keep NLE/DCC bridges. Expand final rendering only for operations whose parity, editability, and quality are proven.

### 16.7 Vertical proof 6: delegated production

Allow the system to take a calibrated, low-risk format from commission to reviewed release candidate within explicit budget and authority. Sample work for human review and automatically escalate novelty, identity, rights, evidence, or capability failures.

## 17. Non-negotiable architecture decisions

1. The system’s primary object is a Living Film Model, not a script, asset list, timeline, or prompt history.
2. The creative brain is a hierarchical blackboard plus deliberation controller, not a linear role-agent chain.
3. The controller selects the next proof based on creative risk and reversibility, not a fixed workflow step.
4. Different formats load different Craft Protocols; no universal script-to-video path exists.
5. The Audiovisual Score is the editorial source of truth above any NLE projection.
6. Sequence, Scene, Shot, Cut, Sound, Graphic, and Performance intents are separate, linked decisions.
7. Media never enters the edit merely because it exists or was generated successfully.
8. Storyboards, style frames, color scripts, sound sketches, animatics, paper edits, dailies, and cut branches are reasoning instruments, not optional documents.
9. Premium faceless video is built from coherent designed sequences, not sentence-level B-roll coverage.
10. Sound, performance, production design, camera, graphics, and editing participate from direction onward.
11. Automation operates through typed work orders, candidate sets, acceptance tests, and receipts.
12. Professional NLEs/DCCs remain first-class craft runtimes; standalone does not mean rebuilding every mature tool.
13. OpenTimelineIO is interchange; it is not the creative model.
14. FFmpeg is media infrastructure; it is not an editor, director, motion designer, or sound department.
15. Model critique produces findings. Human-calibrated preference and accountable approval determine taste.
16. The system may stop, rescope, or request human craft rather than produce a complete weak video.
17. Build creative reasoning and editorial round trip before building a universal renderer.

## 18. Research and implementation foundations

- [Pixar in a Box: The Art of Storytelling](https://www.khanacademy.org/computing/pixar/storytelling) — story structure, visual language, film grammar, storyboarding, and feedback.
- [Pixar film grammar](https://www.khanacademy.org/computing/pixar/storytelling/film-grammar/v/film-grammar-overview) and [storyboarding](https://www.khanacademy.org/partner-content/hass-storytelling/storytelling-pixar-in-a-box/ah-piab-film-grammar/v/storyboarding-scene) — framing, staging, camera movement, editing, composition, and character dynamics.
- [Pixar color scripts](https://www.khanacademy.org/computing/pixar/art-of-lighting/introduction-to-virtual-lighting/v/colorscripts) — light and color as an emotional plan across a film.
- [Walt Disney Animation production process](https://disneyanimation.com/process/) and [Layout](https://disneyanimation.com/process/layout/) — evolving story through editorial/sound and layout as cinematography, staging, composition, performance, and editing.
- [Frame.io stages of editing](https://workflow.frame.io/guide/editing-stages) — assembly, rough cut, intermediate cuts, and picture lock.
- [Frame.io documentary transcript/paper-edit workflow](https://blog.frame.io/2023/10/16/premiere-pro-text-based-editing/) — finding story, character, conflict, tone, and structure from actual material.
- [School of Motion production walkthrough](https://www.schoolofmotion.com/blog/guide-completing-motion-design-project) — concept, moodboard, boards, style frames, and animatic before production.
- [Sony: cinematographer and scene blocking](https://sony-cinematography.com/articles/the-cinematographer-and-scene-blocking/) — subject/object and camera placement designed in anticipation of editing.
- [Blackboard Systems](https://i.stanford.edu/pub/cstr/reports/cs/tr/86/1123/CS-TR-86-1123.pdf) — shared problem state, heterogeneous knowledge sources, and opportunistic control.
- [Dynamic hierarchical long-form story generation](https://aclanthology.org/2025.naacl-long.63/) and [IS-CoT](https://aclanthology.org/2026.acl-long.911.pdf) — macro planning, dynamic guidance, and plan–write–reflect behavior for long-form coherence.
- [Pairwise preference and LLM-evaluator misalignment](https://arxiv.org/html/2403.16950v5) — limitations of uncalibrated LLM judgment.
- [Entity-consistent multi-shot video](https://arxiv.org/html/2605.15199v1) and [Memento](https://arxiv.org/html/2606.14667v1) — long-range subject/scene continuity remains an active generation problem.
- [OpenTimelineIO 0.18](https://opentimelineio.readthedocs.io/en/v0.18.0/) — cut-information interchange, external media references, adapters, and media linkers.
- [Premiere UXP API](https://developer.adobe.com/premiere-pro/uxp/ppro-reference/) — programmatic project, sequence, track, clip, effect, playback, and export access.
- [AYON documentation](https://ayon.ynput.io/) — modular DCC integration, workfiles, loaders, publishers, and scene/version management.
- [MLT Multimedia Framework](https://www.mltframework.org/) — embeddable multitrack audio/video composition engine.
- [Temporal](https://docs.temporal.io/temporal) and [human-in-the-loop workflow](https://docs.temporal.io/ai-cookbook/human-in-the-loop-python) — durable production processes, external activities, and resumable approvals.
- [OpenAssetIO host architecture](https://docs.openassetio.org/OpenAssetIO/notes_for_hosts.html) — identity-based asset references and host/manager separation.
- [OpenColorIO](https://opencolorio.org/) — motion-picture/VFX color-management infrastructure.
- [Unreal cinematics and Movie Render Queue](https://dev.epicgames.com/documentation/unreal-engine/cinematics-and-movie-making-in-unreal-engine) — Sequencer, render passes, scripting, and high-quality cinematic output.
- [FFmpeg filtergraph documentation](https://ffmpeg.org/ffmpeg-filters.html) — deterministic low-level audio/video processing and composition.

