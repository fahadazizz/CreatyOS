# Audiovisual Score API Contract

- `POST/GET /api/v1/projects/{project_id}/score-branches`; `GET /api/v1/score-branches/{branch_id}`.
- `POST/GET /api/v1/score-branches/{branch_id}/events`; `GET /api/v1/score-events/{event_id}`.
- Score events require non-empty `why`, `what`, `how`, and `where_when.{placement,timing,duration,dependency}`.
- Score links are project-scoped; cross-project artifact version, decision, blackboard, or parent-event links are rejected.
- Creating script creative input does not create score branches or score events.
- `POST/GET /api/v1/score-events/{event_id}/lane-entries`; `GET /api/v1/score-branches/{branch_id}/lane-entries`; `GET /api/v1/score-lane-entries/{lane_entry_id}`.
- Score lane entries require non-empty `intent` and lane-specific `content` keys.
- Score lane links are project-scoped; lane entries cannot exist without an existing score event.
- `POST/GET /api/v1/score-events/{event_id}/relationships`; `GET /api/v1/score-branches/{branch_id}/relationships`; `GET /api/v1/score-relationships/{relationship_id}`.
- Score relationships require non-empty `rationale`, `expected_viewer_effect`, `timing_logic`, and `continuity_impact`.
- Score relationships must connect two different events in the same branch; linked proof/decision/artifact references are project-scoped.
- `POST/GET /api/v1/score-branches/{branch_id}/preview-prototypes`; `GET /api/v1/score-preview-prototypes/{prototype_id}`.
- `POST/GET /api/v1/score-preview-prototypes/{prototype_id}/items`; `GET /api/v1/score-preview-items/{preview_item_id}`.
- Preview items require a same-branch score event, non-empty inspection fields, and type-specific body keys; preview records do not create render, asset, or NLE outputs.
- `GET /api/v1/score-preview-prototypes/{prototype_id}/coverage` reports whether every score event in the branch has preview coverage.
