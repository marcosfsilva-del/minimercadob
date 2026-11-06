from collections.abc import Generator
from contextlib import contextmanager
from pathlib import Path

from sqlalchemy import create_engine, text
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

from app.core.config import settings


class Base(DeclarativeBase):
    pass


def _sqlite_path(database_url: str) -> Path | None:
    prefix = "sqlite:///"
    if not database_url.startswith(prefix):
        return None
    return Path(database_url.removeprefix(prefix))


db_path = _sqlite_path(settings.database_url)
if db_path:
    db_path.parent.mkdir(parents=True, exist_ok=True)

engine = create_engine(settings.database_url, future=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False, expire_on_commit=False)


def _ensure_order_delivery_columns() -> None:
    if not settings.database_url.startswith("sqlite:"):
        return

    with engine.begin() as connection:
        columns = {row[1] for row in connection.execute(text("PRAGMA table_info(orders)"))}
        if "delivery_method" not in columns:
            connection.execute(
                text(
                    "ALTER TABLE orders ADD COLUMN delivery_method VARCHAR(20) "
                    "NOT NULL DEFAULT 'retirada'"
                )
            )
        if "delivery_address" not in columns:
            connection.execute(
                text("ALTER TABLE orders ADD COLUMN delivery_address VARCHAR(255)")
            )


def init_database() -> None:
    from app.core import models  # noqa: F401

    Base.metadata.create_all(bind=engine)
    _ensure_order_delivery_columns()


@contextmanager
def session_scope() -> Generator[Session, None, None]:
    session = SessionLocal()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()
