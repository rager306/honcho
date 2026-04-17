import pytest
from hypothesis import given, strategies as st, settings, assume
from datetime import datetime, timezone
from src.utils.representation import ExplicitObservation, ExplicitObservationBase
from pydantic import ValidationError


@given(
    content=st.text(min_size=1, max_size=500),
    rationale=st.one_of(st.none(), st.text(min_size=0, max_size=300)),
    confidence=st.one_of(st.none(), st.sampled_from(["high", "medium", "low"])),
)
def test_explicit_observation_base_roundtrip(content, rationale, confidence):
    """ExplicitObservationBase should preserve all fields through serialization."""
    obs = ExplicitObservationBase(content=content, rationale=rationale, confidence=confidence)
    # Test serialization roundtrip
    dumped = obs.model_dump()
    restored = ExplicitObservationBase.model_validate(dumped)
    assert restored.content == content
    assert restored.rationale == rationale
    assert restored.confidence == confidence


@settings(max_examples=100)
@given(
    content=st.text(min_size=1, max_size=200),
    rationale=st.text(min_size=0, max_size=300),
    confidence=st.sampled_from(["high", "medium", "low"]),
)
def test_confidence_values_are_valid_enum(content, rationale, confidence):
    """Confidence should always accept high/medium/low and reject others."""
    obs = ExplicitObservationBase(content=content, confidence=confidence)
    assert obs.confidence == confidence

    # Invalid values should be rejected
    for invalid in ["very_high", "low-medium", "HIGH", ""]:
        with pytest.raises(ValidationError):
            ExplicitObservationBase(content="test", confidence=invalid)


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


@given(
    content=st.text(min_size=1, max_size=500),
    rationale=st.text(min_size=0, max_size=300),
)
def test_explicit_observation_with_all_fields_str(content, rationale):
    """str() should correctly format observations with various rationale lengths."""
    now = datetime.now(timezone.utc)
    obs = ExplicitObservation(
        content=content,
        rationale=rationale if rationale else None,
        created_at=now,
        message_ids=[1],
        session_name="test",
    )
    result = str(obs)
    assert content in result
