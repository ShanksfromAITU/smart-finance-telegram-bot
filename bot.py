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
        "/balance - show current balance\n\n"
        "Examples:\n"
        "/income 10000 salary scholarship\n"
        "/expense 1500 food lunch\n"
        "/balance"
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


def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("income", income))
    app.add_handler(CommandHandler("expense", expense))
    app.add_handler(CommandHandler("balance", balance))

    print("Smart Finance Bot is running...")
    app.run_polling()


if __name__ == "__main__":
    main()