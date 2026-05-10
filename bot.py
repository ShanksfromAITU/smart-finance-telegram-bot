from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

from config import BOT_TOKEN
from app.finance import FinanceManager


finance_manager = FinanceManager()


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Welcome to Smart Finance Bot!\n\n"
        "Commands:\n"
        "/income amount category description\n"
        "/expense amount category description\n"
        "/balance"
    )


async def income(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        amount = float(context.args[0])
        category = context.args[1]
        description = " ".join(context.args[2:]) if len(context.args) > 2 else "No description"

        finance_manager.add_transaction(
            user_id=update.effective_user.id,
            amount=amount,
            category=category,
            description=description,
            transaction_type="income",
        )

        await update.message.reply_text(
            f"Income added:\n"
            f"Amount: {amount}\n"
            f"Category: {category}\n"
            f"Description: {description}"
        )

    except (IndexError, ValueError):
        await update.message.reply_text(
            "Wrong format.\n"
            "Use: /income amount category description\n"
            "Example: /income 5000 salary monthly payment"
        )


async def expense(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        amount = float(context.args[0])
        category = context.args[1]
        description = " ".join(context.args[2:]) if len(context.args) > 2 else "No description"

        finance_manager.add_transaction(
            user_id=update.effective_user.id,
            amount=amount,
            category=category,
            description=description,
            transaction_type="expense",
        )

        await update.message.reply_text(
            f"Expense added:\n"
            f"Amount: {amount}\n"
            f"Category: {category}\n"
            f"Description: {description}"
        )

    except (IndexError, ValueError):
        await update.message.reply_text(
            "Wrong format.\n"
            "Use: /expense amount category description\n"
            "Example: /expense 1500 food lunch"
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
    app.add_handler(CommandHandler("income", income))
    app.add_handler(CommandHandler("expense", expense))
    app.add_handler(CommandHandler("balance", balance))

    print("Smart Finance Bot is running...")
    app.run_polling()


if __name__ == "__main__":
    main()