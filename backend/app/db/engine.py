from typing import Generator
from sqlmodel import create_engine, Session
from app.core.config import settings


engine = create_engine(
    settings.DATABASE_URL, echo=True, future=True)


def get_db() -> Generator[Session, None, None]:
    with Session(engine, expire_on_commit=False) as session:
        yield session
