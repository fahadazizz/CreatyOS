# Audiovisual Score API Contract

- `POST/GET /api/v1/projects/{project_id}/score-branches`; `GET /api/v1/score-branches/{branch_id}`.
- `POST/GET /api/v1/score-branches/{branch_id}/events`; `GET /api/v1/score-events/{event_id}`.
- Score events require non-empty `why`, `what`, `how`, and `where_when.{placement,timing,duration,dependency}`.
- Score links are project-scoped; cross-project artifact version, decision, blackboard, or parent-event links are rejected.
- Creating script creative input does not create score branches or score events.
- `POST/GET /api/v1/score-events/{event_id}/lane-entries`; `GET /api/v1/score-branches/{branch_id}/lane-entries`; `GET /api/v1/score-lane-entries/{lane_entry_id}`.
- Score lane entries require non-empty `intent` and lane-specific `content` keys.
- Score lane links are project-scoped; lane entries cannot exist without an existing score event.
