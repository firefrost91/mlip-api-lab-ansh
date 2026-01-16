import json
import os
from typing import Any, Dict, List

import litellm
from pydantic import BaseModel, ValidationError, Field, ConfigDict


class Itinerary(BaseModel):
    model_config = ConfigDict(extra="forbid")

    destination: str
    price_range: str
    ideal_visit_times: List[str]
    top_attractions: List[str]


def get_itinerary(destination: str) -> Dict[str, Any]:
    api_key = os.environ.get("GROQ_API_KEY")
    if not api_key:
        raise RuntimeError("Missing GROQ_API_KEY in environment")

    litellm.api_key = api_key

    prompt = f"""
Return ONLY valid JSON (no markdown) with exactly these keys:
- destination (string)
- price_range (string)
- ideal_visit_times (array of strings)
- top_attractions (array of strings)

Destination: {destination}
""".strip()

    response = litellm.completion(
        model="groq/llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
    )

    content = response["choices"][0]["message"]["content"]

    try:
        raw = json.loads(content)
    except json.JSONDecodeError as e:
        # Include model output to debug quickly
        raise ValueError(f"Model did not return valid JSON: {e}\nRaw output:\n{content}") from e

    try:
        itinerary = Itinerary.model_validate(raw)
    except ValidationError as e:
        raise ValueError(f"JSON schema validation failed:\n{e}\nRaw JSON:\n{raw}") from e

    return itinerary.model_dump()
