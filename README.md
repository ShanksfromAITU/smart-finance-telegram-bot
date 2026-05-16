# Smart Finance Telegram Bot

A Python Telegram bot for tracking personal income, expenses, categories, spending limits, reports, CSV export, and expense charts.

This project was developed for Introduction to Programming 2. The main goal of the project is to create a real personal finance assistant that works through Telegram commands.

The bot allows users to add income and expenses, save data, check balance, analyze spending, generate reports, search transactions, set limits, and export history to CSV.

## 1. Create bot token

Open Telegram and message `@BotFather`:

1. Send `/newbot`
2. Choose bot name
3. Choose bot username
4. Copy the token

The token is needed to connect the Python code with your Telegram bot.

## 2. Open in PyCharm

1. Open this folder as a PyCharm project.
2. Create a virtual environment.
3. Install dependencies:

```bash
pip install -r requirements.txt
```

## 3. Add BOT_TOKEN in PyCharm

Go to:

`Run > Edit Configurations > Environment variables`

Add:

```text
BOT_TOKEN=your_token_here
```

Replace `your_token_here` with the token from BotFather.

## 4. Run

Run the bot with:

```bash
python bot.py
```

If everything is correct, the terminal will show that the bot is running.

## Commands

```text
/start
/help
/income 50000 salary May salary
/expense 2500 food lunch
/balance
/categories
/search food
/filter food
/report week
/report month
/chart
/limit food 50000
/limits
/regex lunch|coffee
/export
```

## Project structure

```text
smart_finance_bot/
  app/
    __init__.py
    finance.py
    models.py
    storage.py
  data/
    users.json
    charts/
    exports/
  bot.py
  config.py
  requirements.txt
  README.md
```

## Week 1 – Planning and Project Setup

During Week 1, the project idea was planned and the basic structure was created.

Completed tasks:

- Defined the project idea
- Created Telegram bot using BotFather
- Planned main bot commands
- Designed project folders
- Created the base Python files
- Planned the main classes
- Prepared JSON storage idea

Main idea of the project:

The bot should help users manage personal finances through Telegram. Users should be able to add income, add expenses, check balance, and store all data separately.

Planned main classes:

```text
User
Transaction
Category
FinanceManager
JsonStorage
```

Week 1 was focused on planning and preparing the project base.

## Week 2 – Core Bot Functionality

During Week 2, the main Telegram bot functionality was implemented. The bot became able to receive commands from users and process basic financial operations.

Completed tasks:

- Added Telegram command handlers
- Implemented `/start` command
- Implemented `/help` command
- Implemented income tracking
- Implemented expense tracking
- Added JSON data saving
- Added JSON data loading
- Added balance calculation
- Added separate data storage for each user
- Added basic validation for command format and amount

Main commands added in Week 2:

```text
/start
/help
/income
/expense
/balance
```

Example income command:

```text
/income 50000 salary May salary
```

This command adds income with amount `50000`, category `salary`, and description `May salary`.

Example expense command:

```text
/expense 2500 food lunch
```

This command adds expense with amount `2500`, category `food`, and description `lunch`.

The `/balance` command calculates the user's current balance.

Balance formula:

```text
balance = total income - total expenses
```

Data is stored in JSON format. Each user has separate data because the bot uses Telegram user ID.

Week 2 was focused on creating the basic working version of the bot.

## Week 3 – Analytics and Reporting

During Week 3, analytics and reporting features were added. The bot became able to analyze transactions and show useful financial information.

Completed tasks:

- Added expense categories
- Added category summary
- Added transaction search
- Added transaction filter by category
- Added weekly report
- Added monthly report
- Added charts using Matplotlib

Main commands added in Week 3:

```text
/categories
/search
/filter
/report week
/report month
/chart
```

The `/categories` command shows how much money was spent in each expense category.

Example:

```text
/categories
```

Possible output:

```text
food: 2500
transport: 1000
shopping: 7000
```

The `/search` command searches transactions by keyword.

Example:

```text
/search lunch
```

This command finds transactions where the category or description contains the word `lunch`.

The `/filter` command shows transactions only from one selected category.

Example:

```text
/filter food
```

This command shows all transactions from the `food` category.

The `/report week` command generates a report for the last 7 days.

The `/report month` command generates a report for the last 30 days.

Reports include:

```text
total income
total expense
balance
transactions count
```

The `/chart` command creates an expense chart using Matplotlib. The chart shows expenses by category.

Week 3 was focused on analytics, reports, filtering, searching, and visualization.

## Week 4 – Advanced Features

During Week 4, advanced features were added to make the bot more useful and reliable.

Completed tasks:

- Added spending limits
- Added spending warnings
- Added regex search
- Added CSV export
- Improved exception handling
- Improved input validation
- Improved CSV format for Excel

Main commands added in Week 4:

```text
/limit
/limits
/regex
/export
```

The `/limit` command sets a spending limit for a category.

Example:

```text
/limit food 50000
```

This means the user sets a limit of `50000` for the `food` category.

The `/limits` command shows all current spending limits.

Example:

```text
/limits
```

Possible output:

```text
food: 50000
transport: 10000
```

When the user adds an expense, the bot checks if this category has a limit.

If the user spends more than 80% of the limit, the bot sends a warning.

If the user reaches or exceeds the limit, the bot also sends a warning.

Example:

```text
/expense 45000 food dinner
```

If the food limit is `50000`, the bot warns the user because spending is more than 80% of the limit.

The `/regex` command allows advanced search using regular expressions.

Example:

```text
/regex lunch|coffee
```

This command searches for transactions that contain `lunch` or `coffee`.

Regex search is useful because it can search by patterns, not only simple words.

The `/export` command exports the user's transaction history to a CSV file.

Example:

```text
/export
```

The bot creates and sends a CSV file to the user.

The CSV file contains:

```text
user_number
amount
category
description
transaction_type
created_at
```

The CSV file uses `;` as a separator, so it opens correctly in Excel.

The bot also uses a short `user_number` in CSV instead of a long Telegram user ID, so the file looks cleaner.

Week 4 was focused on advanced functionality, better search, spending control, CSV export, validation, and user experience.

## Data Storage

The project uses JSON files to store user data.

Each user has separate transaction history.

Each transaction contains:

```text
user_id
amount
category
description
transaction_type
created_at
```

Transaction type can be:

```text
income
expense
```

The bot calculates balance and reports based on these saved transactions.

## CSV Export

The bot can export transaction history to CSV using:

```text
/export
```

CSV export allows users to open their financial history in Excel.

The exported file includes:

```text
user_number
amount
category
description
transaction_type
created_at
```

## Technologies Used

```text
Python
Telegram Bot API
python-telegram-bot
JSON
CSV
OOP
Regular Expressions
Matplotlib
PyCharm
GitHub
```

## Run tests

```bash
python -m unittest discover tests
```

## Current Project Status

Weeks 1, 2, 3, and 4 are completed.

The bot can now:

- Add income
- Add expenses
- Store data in JSON
- Show balance
- Show categories
- Search transactions
- Filter by category
- Generate weekly and monthly reports
- Create charts
- Set spending limits
- Show spending warnings
- Search using regex
- Export data to CSV

Week 5 will focus on testing, debugging, final documentation, and project demonstration.