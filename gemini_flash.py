import json
import os
from google import genai

MODEL = os.getenv("GEMINI_FLASH_MODEL", "gemini-2.5-flash")


def _client():
    key = os.getenv("GEMINI_API_KEY")
    if not key:
        raise RuntimeError("GEMINI_API_KEY is missing. Add it to .env")
    return genai.Client(api_key=key)


def generate_outline(prompt: str, character_name: str, setting: str, tone: str, art_style: str):
    client = _client()
    instruction = f"""
Create a 5-panel comic outline.
Story idea: {prompt}
Main character: {character_name}
Setting: {setting}
Tone: {tone}
Art style: {art_style}

Return ONLY valid JSON as an array of exactly 5 objects. Each object must have:
panel_number (integer), title (string), scene_description (string), image_prompt (string).
Keep the same main character and visual appearance across all panels. Do not use markdown fences.
"""
    response = client.models.generate_content(model=MODEL, contents=instruction)
    text = response.text.strip()
    if text.startswith("```"):
        text = text.replace("```json", "").replace("```", "").strip()
    data = json.loads(text)
    if not isinstance(data, list) or len(data) != 5:
        raise ValueError("Gemini did not return exactly 5 panels.")
    return data
