"""
Minimal prompts for the deriver module optimized for speed.

This module contains simplified prompt templates focused only on observation extraction.
NO peer card instructions, NO working representation - just extract observations.
"""

from functools import cache
from inspect import cleandoc as c

from src.utils.tokens import estimate_tokens


def minimal_deriver_prompt(
    peer_id: str,
    messages: str,
) -> str:
    """
    Generate minimal prompt for fast observation extraction.

    Args:
        peer_id: The ID of the user being analyzed.
        messages: All messages in the range (interleaving messages and new turns combined).

    Returns:
        Formatted prompt string for observation extraction.
    """
    return c(
        f"""
Analyze messages from {peer_id} to extract **explicit atomic facts** about them.

[EXPLICIT] DEFINITION: Facts about {peer_id} that can be derived directly from their messages.
   - Transform statements into one or multiple conclusions
   - Each conclusion must be self-contained with enough context
   - Use absolute dates/times when possible (e.g. "June 26, 2025" not "yesterday")

RULES:
- For EACH observation, provide:
  1. **content**: The factual statement about {peer_id}
  2. **rationale**: Brief explanation of HOW you derived this from the source material (what specifically was said/done that supports this)
  3. **confidence**: Level of certainty - "high" (direct statement), "medium" (clear inference), "low" (tentative)
- Properly attribute observations to the correct subject: if it is about {peer_id}, say so. If {peer_id} is referencing someone or something else, make that clear.
- Observations should make sense on their own. Each observation will be used in the future to better understand {peer_id}.
- Extract ALL observations from {peer_id} messages, using others as context.
- Contextualize each observation sufficiently (e.g. "Ann is nervous about the job interview at the pharmacy" not just "Ann is nervous")

OUTPUT FORMAT:
Each observation should have:
- content: The factual statement
- rationale: How this was derived from source material
- confidence: "high", "medium", or "low"

EXAMPLES:
- EXPLICIT: "I just had my 25th birthday last Saturday" → content: "{peer_id} is 25 years old", rationale: "User explicitly stated their age and birthday date", confidence: "high"
- EXPLICIT: "I took my dog for a walk in NYC" → content: "{peer_id} has a dog", rationale: "User mentioned taking their dog for a walk", confidence: "high"; content: "{peer_id} lives in or visits NYC", rationale: "User mentioned walking their dog in NYC", confidence: "high"
- EXPLICIT: "{peer_id} attended college" + general knowledge → content: "{peer_id} completed high school or equivalent", rationale: "Attending college implies completion of prior education", confidence: "medium"

Messages to analyze:
<messages>
{messages}
</messages>
"""
    )


@cache
def estimate_minimal_deriver_prompt_tokens() -> int:
    """Estimate base prompt tokens (cached)."""
    try:
        prompt = minimal_deriver_prompt(
            peer_id="",
            messages="",
        )
        return estimate_tokens(prompt)
    except Exception:
        return 300
