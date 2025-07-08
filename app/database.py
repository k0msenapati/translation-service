from typing import Annotated
from fastapi import Depends
from sqlmodel import Session, create_engine, SQLModel

from app.config import settings

engine = create_engine(
    settings.DATABASE_URL, echo=True, connect_args={"check_same_thread": False}
)


def init_db():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session


db_dependency = Annotated[Session, Depends(get_session)]
