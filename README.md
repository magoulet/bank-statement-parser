# Bank Statement Parser

Python script to analyze dividends from investment accounts: Interactive Brokers (IBKR), CI Direct Investing, and closed accounts.

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

# IBKR Flex Web Service (for automatic sync)
IBKR_FLEX_TOKEN=your_token
IBKR_FLEX_QUERY_ID=your_query_id
```

To get IBKR Flex credentials:
1. Log into IBKR Client Portal
2. Go to Performance & Reports → Flex Queries → Flex Web Service Configuration
3. Generate a token
4. Create a Flex Query with Dividends section, get the Query ID

## Usage

```bash
# One-time: migrate existing IBKR CSV
python scripts/migrate.py

# Periodic: sync latest from IBKR (last 365 days)
python scripts/flex_sync.py sync

# Generate dividend report
python main.py
```

## Workflow

1. **CI Direct** - Manual CSV export (full history)
2. **IBKR** - One-time CSV migration + ongoing Flex sync
3. **Closed Accounts** - Manual CSV export

Data is stored in `ibkr_data.db` (SQLite, gitignored).
