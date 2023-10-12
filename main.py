from dotenv import load_dotenv
from src import TXFetcher

import asyncio
import os
import sys

load_dotenv()

API_KEY = os.environ.get('BSCSCAN_API_KEY')

if __name__ == "__main__":
    fetcher = TXFetcher(API_KEY)
    loop = asyncio.get_event_loop()
    loop.run_until_complete(fetcher.fetch(sys.argv[1]))
