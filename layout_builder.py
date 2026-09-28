import re


def _panel_text(story: str, panel_number: int) -> str:
    pattern = rf"PANEL\s*{panel_number}\b(.*?)(?=\nPANEL\s*{panel_number + 1}\b|\Z)"
    match = re.search(pattern, story, flags=re.IGNORECASE | re.DOTALL)
    return match.group(1).strip() if match else story


def build_comic_layout(outline, story, image_paths):
    layout = []
    for index, panel in enumerate(outline):
        number = panel.get("panel_number", index + 1)
        layout.append({
            "panel_number": number,
            "title": panel.get("title", f"Panel {number}"),
            "scene_description": panel.get("scene_description", ""),
            "image_prompt": panel.get("image_prompt", ""),
            "image_path": image_paths[index] if index < len(image_paths) else None,
            "text": _panel_text(story, number),
        })
    return layout
