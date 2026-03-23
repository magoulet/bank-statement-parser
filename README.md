# Bank Statement Parser

Terminal menu app to sync IBKR flex data, sync transactions to MariaDB, and generate dividend reports.

## Dependencies

```
pip install -r requirements.txt
```

## Setup

1. Clone the repository
2. Copy `.env.example` to `.env` and fill in your config:

```bash
# CI Direct
CI_BASEDIR='/path/to/ci/directory'
CI_FILENAME='statement.csv'

# IBKR
IBKR_BASEDIR='/path/to/ibkr/directory'
IBKR_FILENAME='statement.csv'

# Closed Accounts
CLOSED_BASEDIR='/path/to/closed/directory'
CLOSED_FILENAME='statement.csv'

# IBKR Flex Web Service
IBKR_FLEX_TOKEN=your_token
IBKR_FLEX_QUERY_ID=your_query_id
IBKR_INTRADAY_FLEX_QUERY_ID=your_intraday_query_id

# MySQL (portfolio DB on tars)
MYSQL_HOST=tars
MYSQL_USER=admin
MYSQL_PASSWORD=your_password
```

To get IBKR Flex credentials:
1. Log into IBKR Client Portal
2. Go to Performance & Reports → Flex Queries → Flex Web Service Configuration
3. Generate a token
4. Create a Flex Query with Dividends section, get the Query ID

## Usage

```bash
# Launch the terminal menu
python app.py
```

Inside the menu:

1. Sync IBKR Flex -> SQLite (`scripts/ibkr_data.db`)
2. Sync transactions -> MariaDB (`portfolio.transactions` and `portfolio.contributions`)
3. Generate dividend report

You can still run scripts directly if needed:

```bash
# One-time only historical migration
python scripts/migrate.py

# Manual sync steps
python scripts/flex_sync.py sync
python sync_transactions.py
python report_dividends.py
```
