# Anti-Slop Gate Contract

**Milestone:** 0  
**Status:** doctrine contract for future implementation  
**Related spec:** `docs/specs/product_doctrine_and_anti_slop.md`

## Purpose

This contract defines the minimum gate any future workflow, service, agent, or UI must satisfy before claiming a creative artifact, audiovisual event, sequence, proof, edit branch, or release candidate is ready for the next commitment level.

It is not an API schema yet. It is the product contract Milestone 1 and later schemas must preserve.

## Gate Inputs

A gate review must identify:

- target artifact or event;
- artifact version or branch;
- active Craft Protocol, if known;
- owner or accountable approver;
- source inputs used;
- proposed decision or commitment;
- relevant evidence and constraints;
- proof artifacts available;
- known risks, unknowns, and alternatives.

## Required Checks

The gate must check:

- source-of-truth boundary is preserved;
- script is not being treated as timeline truth;
- each audiovisual event has Why, What, How, and Where/When;
- media has a designed editorial role;
- substantial sequences have a formal idea and progression;
- high-risk commitments have proportionate proof;
- generated or stock material is specific enough for its role;
- music, graphics, text, and animation are not decorative defaults;
- signature moments have alternatives or a documented single-path rationale;
- review is specific to artifacts and moments, not a global score;
- approval authority is separate from generation authority;
- unresolved gaps are surfaced instead of hidden by generic substitution.

## Gate Outcomes

Allowed outcomes:

- **approve:** the artifact may move to the next commitment level within the approved scope.
- **revise:** the artifact needs specific changes before further commitment.
- **request proof:** the system needs a lower-cost artifact or experiment before commitment.
- **block:** the artifact violates a hard invariant or lacks required evidence, authority, material, or quality.
- **accept compromise:** the accountable owner accepts a documented weakness with scope, reason, downstream impact, and revisit condition.
- **escalate:** a human or qualified craft owner must decide.

Disallowed outcomes:

- silent substitution with generic B-roll;
- final render as proof of direction;
- approval by the same generator that created the consequential proposal;
- treating plausible model output as fact, rights clearance, taste evidence, or production approval;
- claiming completion while required proof, authority, or source-of-truth checks are missing.

## Minimum Record

Every gate decision must eventually record:

- decision;
- outcome;
- owner or approving authority;
- target artifact version;
- rationale;
- alternatives considered when relevant;
- evidence or proof reviewed;
- risks accepted or rejected;
- downstream scope affected;
- timestamp or event identity.

Milestone 1 implementation should turn this product contract into concrete schemas, validation rules, persistence, and tests where relevant.
