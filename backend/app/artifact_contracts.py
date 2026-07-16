from typing import Any

from pydantic import BaseModel, ConfigDict, Field, ValidationError, field_validator


class ArtifactBody(BaseModel):
    model_config = ConfigDict(extra="forbid")

    @field_validator("*", mode="before")
    @classmethod
    def reject_blank_strings(cls, value: Any) -> Any:
        if isinstance(value, str):
            stripped = value.strip()
            if not stripped:
                raise ValueError("must not be blank")
            return stripped
        if isinstance(value, list):
            cleaned = []
            for item in value:
                if isinstance(item, str):
                    stripped = item.strip()
                    if not stripped:
                        raise ValueError("list items must not be blank")
                    cleaned.append(stripped)
                else:
                    cleaned.append(item)
            return cleaned
        return value


class CreativeProblemBody(ArtifactBody):
    audience: str
    objective: str
    central_tension_or_opportunity: str
    topic_vs_thesis: str
    constraints: list[str] = Field(min_length=1)
    known_unknowns: list[str] = Field(min_length=1)
    decision_owners: list[str] = Field(min_length=1)
    failure_definition: str
    worth_producing_if: str


class EditorialPointOfViewBody(ArtifactBody):
    position: str
    claims_or_questions: list[str] = Field(min_length=1)
    certainty: str
    source_basis: list[str] = Field(min_length=1)
    narrator_position: str
    audience_relationship: str
    ethical_stance: str
    counter_position: str
    tonal_contract: str


class AudienceExperienceBody(ArtifactBody):
    entry_state: str
    desired_exit_state: str
    evolving_questions: list[str] = Field(min_length=1)
    emotional_curve: list[str] = Field(min_length=1)
    attention_targets: list[str] = Field(min_length=1)
    trust_risks: list[str] = Field(min_length=1)
    memory_anchors: list[str] = Field(min_length=1)


class StoryArgumentModelBody(ArtifactBody):
    premise: str
    controlling_question: str
    stakes: str
    payoff: str
    claims: list[str] = Field(min_length=1)
    evidence_dependencies: list[str] = Field(min_length=1)
    counterclaims: list[str] = Field(min_length=1)
    turns: list[str] = Field(min_length=1)
    omitted_paths: list[str] = Field(min_length=1)


class DirectionBibleBody(ArtifactBody):
    governing_formal_idea: str
    point_of_view_distance: str
    sequence_modes: list[str] = Field(min_length=1)
    visual_principles: list[str] = Field(min_length=1)
    sound_principles: list[str] = Field(min_length=1)
    performance_principles: list[str] = Field(min_length=1)
    tempo_and_restraint: str
    signature_moments: list[str] = Field(min_length=1)
    anti_vision: list[str] = Field(min_length=1)


class VisualLanguageBody(ArtifactBody):
    framing_logic: str
    camera_behavior: str
    composition_rules: list[str] = Field(min_length=1)
    lighting_color_texture: str
    motifs: list[str] = Field(min_length=1)
    transition_principles: list[str] = Field(min_length=1)
    rule_break_conditions: list[str] = Field(min_length=1)


class SoundDirectionBody(ArtifactBody):
    listening_perspective: str
    narration_relationship: str
    ambience_strategy: str
    music_function: str
    silence_strategy: str
    sonic_motifs: list[str] = Field(min_length=1)
    transition_rules: list[str] = Field(min_length=1)
    accessibility_requirements: list[str] = Field(min_length=1)


class ProductionConstraintsBody(ArtifactBody):
    budget_constraints: list[str] = Field(min_length=1)
    schedule_constraints: list[str] = Field(min_length=1)
    legal_constraints: list[str] = Field(min_length=1)
    brand_constraints: list[str] = Field(min_length=1)
    capability_constraints: list[str] = Field(min_length=1)
    delivery_requirements: list[str] = Field(min_length=1)
    explicit_tradeoffs: list[str] = Field(min_length=1)


class RiskRegisterBody(ArtifactBody):
    risks: list[str] = Field(min_length=1)
    impact: str
    likelihood: str
    mitigations: list[str] = Field(min_length=1)
    proof_needed: list[str] = Field(min_length=1)
    owner: str
    status: str


ARTIFACT_CONTRACTS: dict[str, tuple[str, type[ArtifactBody]]] = {
    "creative_problem": ("creative_problem.v1", CreativeProblemBody),
    "editorial_point_of_view": ("editorial_point_of_view.v1", EditorialPointOfViewBody),
    "audience_experience": ("audience_experience.v1", AudienceExperienceBody),
    "story_argument_model": ("story_argument_model.v1", StoryArgumentModelBody),
    "direction_bible": ("direction_bible.v1", DirectionBibleBody),
    "visual_language": ("visual_language.v1", VisualLanguageBody),
    "sound_direction": ("sound_direction.v1", SoundDirectionBody),
    "production_constraints": ("production_constraints.v1", ProductionConstraintsBody),
    "risk_register": ("risk_register.v1", RiskRegisterBody),
}


def validate_artifact_body(
    *, artifact_type: str, schema_version: str, body: dict[str, Any]
) -> dict[str, Any]:
    expected_schema, body_model = ARTIFACT_CONTRACTS[artifact_type]
    if schema_version != expected_schema:
        raise ValueError(
            f"schema_version must be {expected_schema} for artifact_type {artifact_type}"
        )
    try:
        return body_model.model_validate(body).model_dump(mode="json")
    except ValidationError as exc:
        raise ValueError(str(exc)) from exc
