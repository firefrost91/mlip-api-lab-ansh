import json
import os
from typing import Any, Dict
from litellm import completion
import litellm
from dotenv import load_dotenv



# You can replace these with other models as needed but this is the one we suggest for this lab.
MODEL = "groq/llama-3.3-70b-versatile"
api_key = os.environ.get('GROQ_API_KEY')
print("API KEY FOUND:", bool(os.getenv("GROQ_API_KEY")))


def get_itinerary(destination: str) -> Dict[str, Any]:
    """
    Returns a JSON-like dict with keys:
      - destination
      - price_range
      - ideal_visit_times
      - top_attractions
    """
    api_key = os.environ.get('GROQ_API_KEY')
    litellm.api_key = api_key

    prompt = f"""
    Return ONLY valid JSON (no markdown) with exactly these keys:
    - destination (string)
    - price_range (string)
    - ideal_visit_times (array of strings)
    - top_attractions (array of strings)

    Destination: {destination}
    """.strip()

    print("API KEY FOUND:", bool(os.getenv("GROQ_API_KEY")))
    response = litellm.completion(
        model="groq/llama-3.3-70b-versatile",
        messages=[
            {"role": "user", "content": prompt}
        ],
    )

    content = response["choices"][0]["message"]["content"]
    print(json.loads(content))

    # implement litellm call here to generate a structured travel itinerary for the given destination

    # See https://docs.litellm.ai/docs/ for reference.

    

    return json.loads(content)
