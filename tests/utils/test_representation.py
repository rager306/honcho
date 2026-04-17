import pytest
from datetime import datetime, timezone
from src.utils.representation import ExplicitObservation, ExplicitObservationBase


def test_explicit_observation_base_has_rationale_field():
    """ExplicitObservationBase should have optional rationale field."""
    obs = ExplicitObservationBase(content="User is 25 years old", rationale="User explicitly stated their age in the introduction message")
    assert obs.rationale == "User explicitly stated their age in the introduction message"


def test_explicit_observation_base_has_confidence_field():
    """ExplicitObservationBase should have optional confidence field."""
    obs = ExplicitObservationBase(content="User likes coffee", confidence="high")
    assert obs.confidence == "high"


def test_explicit_observation_with_all_fields():
    """ExplicitObservation should support all new fields."""
    now = datetime.now(timezone.utc)
    obs = ExplicitObservation(
        content="User is 25 years old",
        rationale="User explicitly stated their age",
        confidence="high",
        created_at=now,
        message_ids=[1, 2, 3],
        session_name="test-session",
    )
    assert obs.content == "User is 25 years old"
    assert obs.rationale == "User explicitly stated their age"
    assert obs.confidence == "high"


def test_explicit_observation_defaults():
    """Rationale and confidence should default to None."""
    now = datetime.now(timezone.utc)
    obs = ExplicitObservation(
        content="User has a dog",
        created_at=now,
        message_ids=[1],
        session_name="test",
    )
    assert obs.rationale is None
    assert obs.confidence is None


def test_explicit_observation_confidence_validation():
    """Confidence should only accept valid values."""
    from pydantic import ValidationError

    with pytest.raises(ValidationError):
        ExplicitObservationBase(content="test", confidence="very_high")

    # Valid values should work
    for val in ["high", "medium", "low"]:
        obs = ExplicitObservationBase(content="test", confidence=val)
        assert obs.confidence == val


def test_prompt_representation_accepts_observation_with_metadata():
    """PromptRepresentation should accept explicit observations with rationale and confidence."""
    from src.utils.representation import PromptRepresentation

    prompt_rep = PromptRepresentation(
        explicit=[
            ExplicitObservationBase(
                content="User is 25 years old",
                rationale="User stated age directly",
                confidence="high",
            ),
            ExplicitObservationBase(
                content="User likes coffee",
                rationale=None,  # Optional
                confidence=None,  # Optional
            ),
        ]
    )
    assert len(prompt_rep.explicit) == 2
    assert prompt_rep.explicit[0].rationale == "User stated age directly"
    assert prompt_rep.explicit[0].confidence == "high"
    assert prompt_rep.explicit[1].rationale is None


def test_prompt_representation_from_llm_response():
    """Test that PromptRepresentation can be parsed from LLM JSON response."""
    import json
    from src.utils.representation import PromptRepresentation

    # Simulate what an LLM might return
    llm_json = json.dumps({
        "explicit": [
            {
                "content": "User has a dog named Rover",
                "rationale": "User mentioned their dog Rover multiple times",
                "confidence": "high",
            },
            {
                "content": "User lives in NYC",
                "rationale": "User referenced NYC as their location",
                "confidence": "medium",
            },
        ]
    })
    # Pydantic should parse this correctly
    rep = PromptRepresentation.model_validate_json(llm_json)
    assert len(rep.explicit) == 2


def test_from_prompt_representation_preserves_rationale_and_confidence():
    """from_prompt_representation should preserve new fields when creating ExplicitObservation."""
    from src.utils.representation import PromptRepresentation, Representation

    prompt_rep = PromptRepresentation(
        explicit=[
            ExplicitObservationBase(
                content="User is 25 years old",
                rationale="User stated age directly",
                confidence="high",
            ),
        ]
    )

    now = datetime.now(timezone.utc)
    rep = Representation.from_prompt_representation(
        prompt_rep,
        message_ids=[1, 2],
        session_name="test-session",
        created_at=now,
    )

    assert len(rep.explicit) == 1
    assert rep.explicit[0].rationale == "User stated age directly"
    assert rep.explicit[0].confidence == "high"
    assert rep.explicit[0].content == "User is 25 years old"


def test_explicit_observation_str_includes_rationale_when_present():
    """str() should include rationale when it's present."""
    from datetime import datetime, timezone
    from src.utils.representation import ExplicitObservation

    now = datetime.now(timezone.utc)
    obs = ExplicitObservation(
        content="User is 25 years old",
        rationale="User stated their age",
        confidence="high",
        created_at=now,
        message_ids=[1],
        session_name="test",
    )
    str_output = str(obs)
    assert "rationale" in str_output.lower() or "stated their age" in str_output
    assert "high" in str_output


def test_explicit_observation_str_format_without_new_fields():
    """str() should still work correctly when rationale/confidence are None."""
    from datetime import datetime, timezone
    from src.utils.representation import ExplicitObservation

    now = datetime.now(timezone.utc)
    obs = ExplicitObservation(
        content="User is 25 years old",
        rationale=None,
        confidence=None,
        created_at=now,
        message_ids=[1],
        session_name="test",
    )
    str_output = str(obs)
    assert "User is 25 years old" in str_output


def test_str_with_id_includes_rationale_and_confidence():
    """str_with_id() should include rationale and confidence."""
    from datetime import datetime, timezone
    from src.utils.representation import ExplicitObservation

    now = datetime.now(timezone.utc)
    obs = ExplicitObservation(
        id="obs123",
        content="User is 25 years old",
        rationale="User stated their age",
        confidence="high",
        created_at=now,
        message_ids=[1],
        session_name="test",
    )
    output = obs.str_with_id()
    assert "id:obs123" in output
    assert "rationale" in output.lower() or "stated" in output.lower()
    assert "high" in output


def test_format_as_markdown_explicit_includes_confidence():
    """format_as_markdown should display confidence for explicit observations."""
    from datetime import datetime, timezone
    from src.utils.representation import ExplicitObservation, Representation

    now = datetime.now(timezone.utc)
    obs = ExplicitObservation(
        id="obs123",
        content="User is 25 years old",
        rationale="User stated their age",
        confidence="high",
        created_at=now,
        message_ids=[1],
        session_name="test",
    )
    rep = Representation(explicit=[obs])
    md = rep.format_as_markdown()
    assert "high" in md
    assert "25 years old" in md