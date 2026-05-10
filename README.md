# Smart Finance Telegram Bot

Smart Finance Telegram Bot is a personal finance management bot developed in Python.  
The bot helps users track income and expenses directly through Telegram commands.

## Features

- Add income records
- Add expense records
- Store user data in JSON format
- Calculate current balance
- Separate transactions by user
- Basic input validation
- Object-Oriented Programming structure

## Technologies

- Python
- Telegram Bot API
- python-telegram-bot
- JSON
- OOP

## Project Structure

```text
Smart_Finance_Bot/
├── app/
│   ├── __init__.py
│   ├── models.py
│   ├── storage.py
│   └── finance.py
├── data/
│   └── .gitkeep
├── bot.py
├── config.py
├── requirements.txt
├── README.md
└── .gitignore
```

## Commands

```text
/start
/income amount category description
/expense amount category description
/balance
```

## Examples

```text
/income 10000 salary scholarship
/expense 1500 food lunch
/balance
```

## How to Run

Install requirements:

```bash
python -m pip install -r requirements.txt
```

Set Telegram bot token:

```powershell
$env:BOT_TOKEN="your_token_here"
```

Run the bot:

```bash
python bot.py
```

## Week 1 Progress

During Week 1, we created the project structure, connected the Telegram bot, implemented the main classes, added JSON storage, and created basic commands for income, expense, and balance.

## Week 1 Updates

Project setup completed successfully.