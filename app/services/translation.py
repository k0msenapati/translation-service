from typing import List
from openai import OpenAI
from sqlmodel import Session

from app.config import settings
from app.repositories.translation import update_translation_task

TRANSLATION_PROMPT = """
You are a translation assistant. 
Your task is to translate the provided text from the source language to the {target_language}.

Respond with only the translated text.
"""

client = OpenAI(
    api_key=settings.GROQ_API_KEY,
    base_url="https://api.groq.com/openai/v1",
)


def perform_translation(task_id: int, text: str, languages: List[str], db: Session):
    translations = {}

    for lang in languages:
        try:
            response = client.chat.completions.create(
                model="gemma2-9b-it",
                messages=[
                    {
                        "role": "system",
                        "content": TRANSLATION_PROMPT.format(target_language=lang),
                    },
                    {"role": "user", "content": text},
                ],
                max_tokens=1000,
                temperature=0.5,
            )

            translated_text = str(response.choices[0].message.content).strip()
            translations[lang] = translated_text
        except Exception as e:
            print(f"Error translating to {lang}: {str(e)}")
            translations[lang] = f"Error: {str(e)}"

    update_translation_task(
        task_id=task_id, translations=translations, status="completed", db=db
    )
