from fastapi import FastAPI, Query
from googletrans import Translator, LANGUAGES
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Language Translation API")
translator = Translator()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def main():
    return {"message": "Hello World"}

class TranslationSchema(BaseModel):
    text: str
    source_lang: str = None
    target_lang: str


@app.get("/translate")
async def translate_text(
    text: str = Query(..., min_length=1),
    source_lang: str | None = None,
    target_lang: str = Query(..., min_length=2, max_length=2)
):
    """
    Translate text from one language to another using the Google Translate API.

    - **text**: The text to be translated.
    - **source_lang**: The source language code (e.g., 'en', 'es'). If not provided, it will be automatically detected.
    - **target_lang**: The target language code (e.g., 'es', 'fr').
    """
    try:
        translation = translator.translate(text, src=source_lang, dest=target_lang)
        translated_json =  {
            "translated_text": translation.text, 
            "source_lang": translation.src, 
            "target_lang": translation.dest
            }
        return translated_json
    
    except Exception as e:
        return {"error": str(e)}


@app.post("/translate")
async def translate_text(data: TranslationSchema):
    """
    Translate text from one language to another using the Google Translate API.

    Request body:
    {
        "text": "The text to be translated",
        "source_lang": "en", (optional)
        "target_lang": "es"
    }
    """
    try:
        translation = translator.translate(data.text, src=data.source_lang, dest=data.target_lang)
        translated_json =  {
            "translated_text": translation.text, 
            "source_lang": translation.src, 
            "target_lang": translation.dest
            }
        return translated_json
    except Exception as e:
        return {"error": str(e)}


@app.get("/languages")
async def get_language_codes():
    """
    Get a list of all available language codes and their corresponding language names.
    """
    try:
        language_codes = {code: lang.capitalize() for code, lang in LANGUAGES.items()}
        return {"language_codes": language_codes}
    except Exception as e:
        return {"error": str(e)}
    
