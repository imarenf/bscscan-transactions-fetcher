from sqlalchemy.ext.asyncio import (
    create_async_engine,
    AsyncEngine,
    AsyncAttrs
)

from sqlalchemy.orm import (
    Mapped,
    DeclarativeBase,
    mapped_column
)

import asyncpg
import os


class Base(AsyncAttrs, DeclarativeBase):
    pass


class Transaction(Base):
    __tablename__ = "transactions"

    id: Mapped[int] = mapped_column(primary_key=True)
    hash: Mapped[str] = mapped_column(unique=True)
    from_: Mapped[str]
    to_: Mapped[str]
    status: Mapped[int]
    confirmations: Mapped[int]


async def create_database_if_not_exist(db_username: str, db_password: str, db_host: str, db_port: str,
                                       db_name: str) -> None:
    conn = await asyncpg.connect(user=db_username, password=db_password, host=db_host, port=db_port)
    try:
        await conn.execute(f'CREATE DATABASE {db_name}')
    except asyncpg.exceptions.DuplicateDatabaseError:
        pass
    finally:
        await conn.close()


async def init_db() -> AsyncEngine:
    db_username = os.environ.get('POSTGRES_USER')
    db_password = os.environ.get('POSTGRES_PASSWORD')
    db_host = os.environ.get('POSTGRES_HOST')
    db_port = os.environ.get('POSTGRES_PORT')
    db_name = os.environ.get('POSTGRES_DB_NAME')

    await create_database_if_not_exist(db_username, db_password, db_host, db_port, db_name)

    engine = create_async_engine(
        f'postgresql+asyncpg://{db_username}:{db_password}@{db_host}:{db_port}/{db_name}',
        future=True
    )

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    return engine
