# ComicCraft - AI Comic Story Creator

## Folder structure

```text
ComicCraft/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── routes.py
│   ├── gemini_flash.py
│   ├── gemini_pro.py
│   ├── image_generator.py
│   ├── layout_builder.py
│   └── exporters.py
├── templates/
│   ├── index.html
│   ├── comic_preview.html
│   └── export_success.html
├── static/
│   ├── panels/
│   └── exports/
├── fonts/
├── .env.example
├── .gitignore
├── requirements.txt
└── README.md
```

## Windows setup

```powershell
python -m venv env
env\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
```

Open `.env` and add your Gemini API key and Hugging Face token.

## Run

```powershell
python -m uvicorn app.main:app --reload
```

Open:
- http://127.0.0.1:8000
- http://127.0.0.1:8000/docs
- http://127.0.0.1:8000/health

The app generates a 5-panel outline with Gemini Flash, expands it with Gemini Pro, generates images through Hugging Face Stable Diffusion, builds the layout, and exports a PDF.
