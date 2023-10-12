from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlalchemy.exc import IntegrityError
from typing import (
    TypeVar,
    List
)
from src.db_init import (
    init_db,
    Transaction
)

_DBC = TypeVar("_DBC", bound="DBClient")


class DBClient:
    def __init__(self) -> None:
        self.engine = None
        self.session_maker = None

    async def __aenter__(self) -> _DBC:
        self.engine = await init_db()
        self.session_maker = async_sessionmaker(self.engine, expire_on_commit=False)
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        pass

    async def insert_transaction_chunk(self, tx_list: List[dict]) -> None:
        if not self.engine:
            raise AssertionError
        async with self.session_maker() as session:
            async with session.begin():
                try:
                    session.add_all(
                        [Transaction(**tx_data) for tx_data in tx_list]
                    )
                    await session.commit()
                except IntegrityError:
                    # transactions duplicate case
                    pass
                finally:
                    await session.close()
