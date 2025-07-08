from fastapi import BackgroundTasks, HTTPException, APIRouter

from app.schemas.translation import (
    TaskResponse,
    TranslationRequest,
    TranslationResponse,
    TranslationStatus,
)
from app.repositories.translation import create_translation_task, get_translation_task
from app.services.translation import perform_translation
from app.database import db_dependency

router = APIRouter(tags=["translation"])


@router.post("/translate", response_model=TaskResponse)
def translate(
    request: TranslationRequest, background_tasks: BackgroundTasks, db: db_dependency
):
    task = create_translation_task(
        db=db, text=request.text, languages=request.languages
    )

    if not task.id:
        raise HTTPException(status_code=500, detail="Failed to create translation task")

    background_tasks.add_task(
        perform_translation, task.id, request.text, request.languages, db
    )

    return {"task_id": task.id}


@router.get("/status/{task_id}", response_model=TranslationStatus)
def get_translate_status(task_id: int, db: db_dependency):
    task = get_translation_task(db=db, task_id=task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return {
        "task_id": task.id,
        "status": task.status,
        "translations": task.translations if task.status == "completed" else None,
    }


@router.get("/content/{task_id}", response_model=TranslationResponse)
def get_translate_content(task_id: int, db: db_dependency):
    task = get_translation_task(db=db, task_id=task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task
