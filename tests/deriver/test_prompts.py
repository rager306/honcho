import pytest
from src.deriver.prompts import minimal_deriver_prompt


def test_minimal_deriver_prompt_requests_rationale():
    """Prompt should instruct LLM to provide rationale for each observation."""
    prompt = minimal_deriver_prompt(peer_id="user123", messages="test message")
    assert "rationale" in prompt.lower() or "reasoning" in prompt.lower()


def test_minimal_deriver_prompt_requests_confidence():
    """Prompt should instruct LLM to provide confidence level for each observation."""
    prompt = minimal_deriver_prompt(peer_id="user123", messages="test message")
    assert "confidence" in prompt.lower()


def test_minimal_deriver_prompt_includes_output_format():
    """Prompt should specify output format with content, rationale, confidence."""
    prompt = minimal_deriver_prompt(peer_id="user123", messages="test")
    assert "content" in prompt.lower()
    assert "confidence" in prompt.lower()
    assert "high" in prompt.lower() or "medium" in prompt.lower() or "low" in prompt.lower()