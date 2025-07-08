from typing import Dict, List, Optional
from sqlmodel import Field, SQLModel, JSON, Column


class TranslationTask(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    text: str
    languages: List[str] = Field(sa_column=Column(JSON))
    status: str = "pending"
    translations: Dict[str, str] = Field(default_factory=dict, sa_column=Column(JSON))
