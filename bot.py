import os

import matplotlib.pyplot as plt
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

from config import BOT_TOKEN
from app.finance import FinanceManager


finance_manager = FinanceManager()


def get_help_text() -> str:
    return (
        "Smart Finance Bot Commands:\n\n"
        "/start - start the bot\n"
        "/help - show command list\n"
        "/income amount category description - add income\n"
        "/expense amount category description - add expense\n"
        "/balance - show current balance\n"
        "/categories - show expense categories summary\n"
        "/search keyword - search transactions\n"
        "/filter category - filter transactions by category\n"
        "/report week - show weekly report\n"
        "/report month - show monthly report\n"
        "/chart - create expense chart\n\n"
        "Examples:\n"
        "/income 10000 salary scholarship\n"
        "/expense 1500 food lunch\n"
        "/search lunch\n"
        "/filter food\n"
        "/report week\n"
        "/chart"
    )


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Welcome to Smart Finance Bot!\n\n"
        "This bot helps you track your income and expenses.\n\n"
        + get_help_text()
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(get_help_text())


async def income(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        if len(context.args) < 2:
            raise IndexError

        amount = float(context.args[0])
        category = context.args[1]
        description = " ".join(context.args[2:]) if len(context.args) > 2 else "No description"

        transaction = finance_manager.add_transaction(
            user_id=update.effective_user.id,
            amount=amount,
            category=category,
            description=description,
            transaction_type="income",
        )

        await update.message.reply_text(
            "Income added successfully!\n\n"
            f"Amount: {transaction.amount}\n"
            f"Category: {transaction.category}\n"
            f"Description: {transaction.description}\n"
            f"Date: {transaction.created_at}"
        )

    except IndexError:
        await update.message.reply_text(
            "Wrong command format.\n\n"
            "Use:\n"
            "/income amount category description\n\n"
            "Example:\n"
            "/income 10000 salary scholarship"
        )

    except ValueError:
        await update.message.reply_text(
            "Invalid amount.\n\n"
            "Amount must be a positive number.\n\n"
            "Example:\n"
            "/income 10000 salary scholarship"
        )


async def expense(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        if len(context.args) < 2:
            raise IndexError

        amount = float(context.args[0])
        category = context.args[1]
        description = " ".join(context.args[2:]) if len(context.args) > 2 else "No description"

        transaction = finance_manager.add_transaction(
            user_id=update.effective_user.id,
            amount=amount,
            category=category,
            description=description,
            transaction_type="expense",
        )

        await update.message.reply_text(
            "Expense added successfully!\n\n"
            f"Amount: {transaction.amount}\n"
            f"Category: {transaction.category}\n"
            f"Description: {transaction.description}\n"
            f"Date: {transaction.created_at}"
        )

    except IndexError:
        await update.message.reply_text(
            "Wrong command format.\n\n"
            "Use:\n"
            "/expense amount category description\n\n"
            "Example:\n"
            "/expense 1500 food lunch"
        )

    except ValueError:
        await update.message.reply_text(
            "Invalid amount.\n\n"
            "Amount must be a positive number.\n\n"
            "Example:\n"
            "/expense 1500 food lunch"
        )


async def balance(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    current_balance = finance_manager.get_balance(user_id)

    await update.message.reply_text(
        f"Your current balance is: {current_balance}"
    )


async def categories(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    summary = finance_manager.get_expense_categories_summary(user_id)

    if not summary:
        await update.message.reply_text("No expense categories found.")
        return

    message = "Expense categories summary:\n\n"

    for category, amount in summary.items():
        message += f"{category}: {amount}\n"

    await update.message.reply_text(message)


async def search(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text(
            "Wrong command format.\n\n"
            "Use:\n"
            "/search keyword\n\n"
            "Example:\n"
            "/search lunch"
        )
        return

    user_id = update.effective_user.id
    keyword = " ".join(context.args)
    results = finance_manager.search_transactions(user_id, keyword)

    if not results:
        await update.message.reply_text("No transactions found.")
        return

    message = f"Search results for '{keyword}':\n\n"

    for transaction in results:
        sign = "+" if transaction["transaction_type"] == "income" else "-"
        message += (
            f"{sign}{transaction['amount']} | "
            f"{transaction['category']} | "
            f"{transaction['description']} | "
            f"{transaction['created_at']}\n"
        )

    await update.message.reply_text(message)


async def filter_category(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text(
            "Wrong command format.\n\n"
            "Use:\n"
            "/filter category\n\n"
            "Example:\n"
            "/filter food"
        )
        return

    user_id = update.effective_user.id
    category = context.args[0]
    results = finance_manager.filter_by_category(user_id, category)

    if not results:
        await update.message.reply_text("No transactions found for this category.")
        return

    message = f"Transactions in category '{category}':\n\n"

    for transaction in results:
        sign = "+" if transaction["transaction_type"] == "income" else "-"
        message += (
            f"{sign}{transaction['amount']} | "
            f"{transaction['description']} | "
            f"{transaction['created_at']}\n"
        )

    await update.message.reply_text(message)


async def report(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        if not context.args:
            raise ValueError

        period = context.args[0].lower()
        report_data = finance_manager.get_report(
            user_id=update.effective_user.id,
            period=period,
        )

        await update.message.reply_text(
            f"{period.capitalize()} report:\n\n"
            f"Total income: {report_data['total_income']}\n"
            f"Total expense: {report_data['total_expense']}\n"
            f"Balance: {report_data['balance']}\n"
            f"Transactions count: {report_data['transactions_count']}"
        )

    except ValueError:
        await update.message.reply_text(
            "Wrong command format.\n\n"
            "Use:\n"
            "/report week\n"
            "or\n"
            "/report month"
        )


async def chart(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    summary = finance_manager.get_expense_categories_summary(user_id)

    if not summary:
        await update.message.reply_text("No expense data for chart.")
        return

    os.makedirs("data/charts", exist_ok=True)
    chart_path = f"data/charts/expenses_{user_id}.png"

    categories_list = list(summary.keys())
    amounts = list(summary.values())

    plt.figure(figsize=(8, 5))
    plt.bar(categories_list, amounts)
    plt.title("Expenses by Category")
    plt.xlabel("Category")
    plt.ylabel("Amount")
    plt.tight_layout()
    plt.savefig(chart_path)
    plt.close()

    with open(chart_path, "rb") as photo:
        await update.message.reply_photo(photo=photo)


def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("income", income))
    app.add_handler(CommandHandler("expense", expense))
    app.add_handler(CommandHandler("balance", balance))
    app.add_handler(CommandHandler("categories", categories))
    app.add_handler(CommandHandler("search", search))
    app.add_handler(CommandHandler("filter", filter_category))
    app.add_handler(CommandHandler("report", report))
    app.add_handler(CommandHandler("chart", chart))

    print("Smart Finance Bot is running...")
    app.run_polling()


if __name__ == "__main__":
    main()