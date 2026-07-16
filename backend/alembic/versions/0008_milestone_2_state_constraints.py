"""milestone 2 state constraints

Revision ID: 0008_milestone_2_state_constraints
Revises: 0007_human_checkpoints
Create Date: 2026-07-16
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "0008_milestone_2_state_constraints"
down_revision: str | None = "0007_human_checkpoints"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    with op.batch_alter_table("blackboard_entries") as batch_op:
        batch_op.create_check_constraint(
            "ck_blackboard_entries_entry_type",
            "entry_type IN ('observation','proposal','contradiction','missing_information','risk','issue','proof_request','task_recommendation')",
        )
        batch_op.create_check_constraint(
            "ck_blackboard_entries_status",
            "status IN ('open','accepted','rejected','resolved','superseded')",
        )
        batch_op.create_check_constraint(
            "ck_blackboard_entries_severity",
            "severity IN ('low','medium','high','critical')",
        )
    with op.batch_alter_table("deliberation_records") as batch_op:
        batch_op.create_check_constraint(
            "ck_deliberation_records_phase",
            "phase IN ('sense','frame','diverge','externalize','experience','critique','decide','commit','propagate','reopen')",
        )
        batch_op.create_check_constraint(
            "ck_deliberation_records_status",
            "status IN ('open','recorded','superseded')",
        )
    with op.batch_alter_table("specialist_proposals") as batch_op:
        batch_op.create_check_constraint(
            "ck_specialist_proposals_specialist_type",
            "specialist_type IN ('creative_director','story_argument','editorial','visual_direction','sound_direction','producer','critic')",
        )
        batch_op.create_check_constraint(
            "ck_specialist_proposals_status",
            "status IN ('submitted')",
        )
    with op.batch_alter_table("human_checkpoints") as batch_op:
        batch_op.create_check_constraint(
            "ck_human_checkpoints_checkpoint_type",
            "checkpoint_type IN ('project_thesis','creative_route','audience_promise','final_treatment','visual_language','production_plan','edit_direction','final_release')",
        )
        batch_op.create_check_constraint(
            "ck_human_checkpoints_decision_status",
            "decision_status IN ('pending','approved','revision_requested','blocked')",
        )


def downgrade() -> None:
    with op.batch_alter_table("human_checkpoints") as batch_op:
        batch_op.drop_constraint("ck_human_checkpoints_decision_status", type_="check")
        batch_op.drop_constraint("ck_human_checkpoints_checkpoint_type", type_="check")
    with op.batch_alter_table("specialist_proposals") as batch_op:
        batch_op.drop_constraint("ck_specialist_proposals_status", type_="check")
        batch_op.drop_constraint("ck_specialist_proposals_specialist_type", type_="check")
    with op.batch_alter_table("deliberation_records") as batch_op:
        batch_op.drop_constraint("ck_deliberation_records_status", type_="check")
        batch_op.drop_constraint("ck_deliberation_records_phase", type_="check")
    with op.batch_alter_table("blackboard_entries") as batch_op:
        batch_op.drop_constraint("ck_blackboard_entries_severity", type_="check")
        batch_op.drop_constraint("ck_blackboard_entries_status", type_="check")
        batch_op.drop_constraint("ck_blackboard_entries_entry_type", type_="check")
