from sqlmodel import Session

from app.models.translation import TranslationTask


def create_translation_task(db: Session, text: str, languages: list[str]):
    task = TranslationTask(text=text, languages=languages)

    db.add(task)
    db.commit()
    db.refresh(task)
    return task


def get_translation_task(db: Session, task_id: int):
    return db.get(TranslationTask, task_id)


def update_translation_task(
    db: Session, task_id: int, status: str, translations: dict[str, str]
):
    task = db.get(TranslationTask, task_id)
    if task:
        task.status = status
        task.translations = translations
        db.commit()
        db.refresh(task)
    return task
