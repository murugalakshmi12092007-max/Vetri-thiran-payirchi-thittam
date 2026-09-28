from pathlib import Path
from fpdf import FPDF
from datetime import datetime
import os

BASE_DIR = Path(__file__).resolve().parent.parent
EXPORT_DIR = BASE_DIR / "static" / "exports"
FONT_DIR = BASE_DIR / "fonts"
EXPORT_DIR.mkdir(parents=True, exist_ok=True)


def _font_path():
    candidates = [
        FONT_DIR / "DejaVuSans.ttf",
        Path("C:/Windows/Fonts/arial.ttf"),
        Path("C:/Windows/Fonts/calibri.ttf"),
    ]
    for path in candidates:
        if path.exists():
            return path
    return None


def save_pdf(layout, title="ComicCraft Comic"):
    pdf = FPDF(format="A4")
    pdf.set_auto_page_break(auto=True, margin=15)
    font_path = _font_path()
    if font_path:
        pdf.add_font("ComicFont", "", str(font_path))
        font_name = "ComicFont"
    else:
        font_name = "Helvetica"

    for panel in layout:
        pdf.add_page()
        pdf.set_font(font_name, size=18)
        pdf.multi_cell(0, 10, f"Panel {panel['panel_number']}: {panel['title']}", align="C")
        image_url = panel.get("image_path")
        if image_url:
            image_file = BASE_DIR / image_url.lstrip("/").replace("/", os.sep)
            if image_file.exists():
                pdf.image(str(image_file), x=15, y=35, w=180, h=100, keep_aspect_ratio=True)
                pdf.set_y(142)
        pdf.set_font(font_name, size=11)
        pdf.multi_cell(0, 7, f"Scene: {panel.get('scene_description', '')}")
        pdf.ln(2)
        pdf.multi_cell(0, 7, panel.get("text", ""))

    filename = f"comic_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
    path = EXPORT_DIR / filename
    pdf.output(str(path))
    return f"/static/exports/{filename}"
