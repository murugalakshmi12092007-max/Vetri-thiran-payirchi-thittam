from pathlib import Path
from fastapi import APIRouter, Form, Request, HTTPException
from fastapi.responses import RedirectResponse
from pydantic import BaseModel
from .gemini_flash import generate_outline
from .gemini_pro import generate_story
from .image_generator import generate_image
from .layout_builder import build_comic_layout
from .exporters import save_pdf

BASE_DIR = Path(__file__).resolve().parent.parent
router = APIRouter()


class PromptRequest(BaseModel):
    story_prompt: str
    character_name: str
    setting: str
    tone: str
    art_style: str


def _generate(data: PromptRequest):
    outline = generate_outline(data.story_prompt, data.character_name, data.setting, data.tone, data.art_style)
    story = generate_story(outline, data.character_name, data.tone)
    images = [generate_image(panel["image_prompt"], panel["panel_number"]) for panel in outline]
    layout = build_comic_layout(outline, story, images)
    pdf_path = save_pdf(layout, title=data.story_prompt)
    return outline, story, layout, pdf_path


@router.get("/")
async def home(request: Request):
    return request.app.state.templates.TemplateResponse("index.html", {"request": request})


@router.post("/generate")
async def generate(
    request: Request,
    story_prompt: str = Form(...),
    character_name: str = Form(...),
    setting: str = Form(...),
    tone: str = Form(...),
    art_style: str = Form(...),
):
    try:
        data = PromptRequest(
            story_prompt=story_prompt,
            character_name=character_name,
            setting=setting,
            tone=tone,
            art_style=art_style,
        )
        outline, story, layout, pdf_path = _generate(data)
        return request.app.state.templates.TemplateResponse(
            "comic_preview.html",
            {"request": request, "layout": layout, "pdf_path": pdf_path, "story": story},
        )
    except Exception as exc:
        return request.app.state.templates.TemplateResponse(
            "index.html", {"request": request, "error": str(exc)}, status_code=500
        )


@router.post("/generate-comic/json")
async def generate_json(data: PromptRequest):
    try:
        _, story, layout, pdf_path = _generate(data)
        return {"success": True, "layout": layout, "story": story, "pdf_path": pdf_path}
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))


@router.get("/export-success")
async def export_success(request: Request):
    return request.app.state.templates.TemplateResponse("export_success.html", {"request": request})


@router.get("/test-image")
async def test_image(prompt: str = "a cute fox in an enchanted forest"):
    try:
        path = generate_image(prompt, 0)
        return {"success": True, "image_path": path}
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))
