from typing import Dict, List
from pydantic import BaseModel


class TranslationRequest(BaseModel):
    text: str
    languages: List[str]


class TaskResponse(BaseModel):
    task_id: int


class TranslationStatus(BaseModel):
    task_id: int
    status: str
    translations: Dict[str, str] | None = None


class TranslationResponse(BaseModel):
    id: int
    text: str
    languages: List[str]
    status: str = "pending"
    translations: Dict[str, str] = {}
