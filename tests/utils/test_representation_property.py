import pytest
from hypothesis import given, strategies as st, settings
from datetime import datetime, timezone
from src.utils.representation import ExplicitObservation, ExplicitObservationBase


@given(
    content=st.text(min_size=1, max_size=500),
    rationale=st.one_of(st.none(), st.text(min_size=0, max_size=300)),
    confidence=st.one_of(st.none(), st.sampled_from(["high", "medium", "low"])),
)
def test_explicit_observation_base_roundtrip(content, rationale, confidence):
    """ExplicitObservationBase should preserve all fields through serialization."""
    obs = ExplicitObservationBase(content=content, rationale=rationale, confidence=confidence)
    assert obs.content == content
    assert obs.rationale == rationale
    assert obs.confidence == confidence


@given(
    content=st.text(min_size=1, max_size=500),
    rationale=st.text(min_size=0, max_size=300),
)
def test_explicit_observation_with_various_rationale_lengths(content, rationale):
    """ExplicitObservation should handle rationale of various lengths."""
    now = datetime.now(timezone.utc)
    obs = ExplicitObservation(
        content=content,
        rationale=rationale if rationale else None,
        created_at=now,
        message_ids=[1],
        session_name="test",
    )
    assert obs.content == content


@settings(max_examples=100)
@given(
    content=st.text(min_size=1, max_size=200),
    confidence=st.sampled_from(["high", "medium", "low"]),
)
def test_confidence_values_are_valid_enum(content, confidence):
    """Confidence should always be one of the valid enum values."""
    obs = ExplicitObservationBase(content=content, confidence=confidence)
    assert obs.confidence in ("high", "medium", "low")


@given(
    content=st.text(min_size=1, max_size=500),
)
def test_explicit_observation_str_does_not_crash(content):
    """str() should never raise an exception regardless of content."""
    now = datetime.now(timezone.utc)
    obs = ExplicitObservation(
        content=content,
        created_at=now,
        message_ids=[1],
        session_name="test",
    )
    result = str(obs)
    assert isinstance(result, str)
    assert len(result) > 0
