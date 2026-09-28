import os
from google import genai

MODEL = os.getenv("GEMINI_PRO_MODEL", "gemini-2.5-pro")


def _client():
    key = os.getenv("GEMINI_API_KEY")
    if not key:
        raise RuntimeError("GEMINI_API_KEY is missing. Add it to .env")
    return genai.Client(api_key=key)


def generate_story(outline, character_name: str, tone: str):
    client = _client()
    prompt = f"""
Write the detailed text for a 5-panel comic using this outline.
Main character: {character_name}
Tone: {tone}

For every panel return a section with exactly these labels:
PANEL <number>
TITLE: ...
SCENE: ...
CAPTION: ...
NARRATION: ...
DIALOGUE: ...

Keep the story coherent and concise. Dialogue should be suitable for a general audience.
Outline:
{outline}
"""
    response = client.models.generate_content(model=MODEL, contents=prompt)
    return response.text.strip()
