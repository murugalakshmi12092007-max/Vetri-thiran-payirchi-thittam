import os
import re
from pathlib import Path
from huggingface_hub import InferenceClient

BASE_DIR = Path(__file__).resolve().parent.parent
OUTPUT_DIR = BASE_DIR / "static" / "panels"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

MODEL = os.getenv("HF_IMAGE_MODEL", "stabilityai/stable-diffusion-xl-base-1.0")


def _safe_name(text: str) -> str:
    text = re.sub(r"[^a-zA-Z0-9_-]+", "_", text).strip("_")
    return text[:70] or "panel"


def generate_image(image_prompt: str, panel_number: int) -> str:
    token = os.getenv("HF_API_KEY")
    if not token:
        raise RuntimeError("HF_API_KEY is missing. Add it to .env")

    client = InferenceClient(model=MODEL, token=token)
    prompt = (
        "Comic book panel illustration, clean composition, expressive characters, "
        "consistent character design, detailed background, no text, no watermark. "
        + image_prompt
    )
    image = client.text_to_image(prompt)
    filename = f"panel_{panel_number}_{_safe_name(image_prompt)}.png"
    path = OUTPUT_DIR / filename
    image.save(path)
    return f"/static/panels/{filename}"
