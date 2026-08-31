# src/llm_response.py
import json
import re

def parse_llm_json(response):
    """Extracts and parses JSON from the LLM response, tolerating
    different formats across SDK/provider versions (string, already-parsed
    dict, or list of content blocks, or JSON wrapped in ```json ... ```)."""
    content = response.choices[0].message.content

    if isinstance(content, dict):
        return content  # already parsed

    if isinstance(content, list):
        content = "".join(
            block.get("text", "") if isinstance(block, dict) else str(block)
            for block in content
        )

    if not content or not content.strip():
        raise ValueError(f"LLM returned empty content. Raw response: {response}")

    text = content.strip()
    fence_match = re.search(r"```(?:json)?\s*(.*?)\s*```", text, re.DOTALL)
    if fence_match:
        text = fence_match.group(1)

    return json.loads(text)