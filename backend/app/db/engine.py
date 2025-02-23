import os
from typing import Generator
from sqlmodel import create_engine, Session
from dotenv import load_dotenv
from app.core.config import settings

load_dotenv()
ENV = os.getenv("ENV", "dev")

engine = create_engine(
    settings.DATABASE_URL, echo=False if ENV == "prod" else True, future=True)


def get_db() -> Generator[Session, None, None]:
    with Session(engine, expire_on_commit=False) as session:
        yield session
