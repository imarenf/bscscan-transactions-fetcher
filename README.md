# Transactions fetcher
## Receives information about new transactions bscscan.com and stores them into PostgreSQL DataBase

### Pre-installation requirements:
 - Python >= 3.9 (3.10 recommended) 
 - PostgreSQL >= 10 (14 recommended)

### Installation:
 - Create and activate virtual environment
 - Clone the repository
 - Run __pip install -r requirements.txt__
 - Rename __.env.example__ to __.env__ and fill in your BscScan API Key and DataBase name (you can pick one that you like)
To find out how to get the API key, follow the [creating an account](https://docs.bscscan.com/getting-started/creating-an-account) and [getting an API key](https://docs.bscscan.com/getting-started/viewing-api-usage-statistics)

### Run:
 - python main.py `<address>`
   (Put here the address whose transactions you want to retrieve)