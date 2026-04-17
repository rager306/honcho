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