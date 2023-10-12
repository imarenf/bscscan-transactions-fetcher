from bscscan import BscScan
from bscscan.core.async_client import AsyncClient
from src.constants import (
    MAX_RESP_CNT,
    MAX_BLOCK_NUM
)
from src.dbclient import DBClient
from src.txserializer import TXSerializer
from typing import Tuple

import asyncio


class TXFetcher:
    def __init__(self, api_key: str) -> None:
        self.api_key = api_key
        self.serializer = TXSerializer()
        self.tasks = []

    async def request_and_insert_chunk(self, api_client: AsyncClient, address: str, start_block: int,
                                       end_block: int, db_client: DBClient) -> Tuple[int, int]:
        resp = await api_client.get_normal_txs_by_address(
            address=address,
            startblock=start_block,
            endblock=end_block,
            sort='asc'
        )
        tx_list = [self.serializer.serialize_tx_data(tx) for tx in resp]
        tx_list = list(filter(lambda x: x != {}, tx_list))
        self.tasks.append(asyncio.create_task(db_client.insert_transaction_chunk(tx_list)))
        return len(resp), int(resp[-1]['blockNumber'])

    async def fetch(self, address: str):
        start_block = 0
        size = MAX_RESP_CNT
        end_block = MAX_BLOCK_NUM
        async with BscScan(self.api_key, asynchronous=True) as api_client, DBClient() as db_client:
            while size == MAX_RESP_CNT:
                size, start_block = await self.request_and_insert_chunk(
                    api_client=api_client,
                    address=address,
                    start_block=start_block,
                    end_block=end_block,
                    db_client=db_client
                )
        await asyncio.gather(*self.tasks)
