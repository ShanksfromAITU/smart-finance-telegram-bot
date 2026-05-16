import os
import matplotlib.pyplot as plt

from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

from config import BOT_TOKEN
from app.finance import FinanceManager


finance_manager = FinanceManager()


def get_help_text() -> str:
    return (
        "🤖 Smart Finance Bot Commands\n\n"
        "🚀 /start - start the bot\n"
        "ℹ️ /help - show command list\n"
        "💵 /income [amount] [category] [description] - add income\n"
        "💸 /expense [amount] [category] [description] - add expense\n"
        "💰 /balance - show current balance\n"
        "📂 /categories - show expense categories summary\n"
        "🔎 /search [keyword] - search transactions\n"
        "🏷 /filter [category] - filter transactions by category\n"
        "📊 /report [week/month] - show financial report\n"
        "📈 /chart - create expense chart\n"
        "⚠️ /limit [category] [amount] - set spending limit\n"
        "📌 /limits - show spending limits\n"
        "🧩 /regex [pattern] - search transactions using regex\n"
        "📤 /export - export transactions to CSV\n\n"
        "Examples:\n"
        "💵 /income 10000 salary scholarship\n"
        "💸 /expense 1500 food lunch\n"
        "🔎 /search lunch\n"
        "🏷 /filter food\n"
        "📊 /report week\n"
        "📈 /chart\n"
        "⚠️ /limit food 5000\n"
        "📌 /limits\n"
        "🧩 /regex lunch|coffee\n"
        "📤 /export"
    )


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Welcome to Smart Finance Bot!\n\n"
        "This bot helps you track your income, expenses, balance, reports, charts, and spending limits.\n\n"
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
            "✅ Income added successfully!\n\n"
            "💵 Amount: {} KZT\n"
            "📂 Category: {}\n"
            "📝 Description: {}\n"
            "📅 Date: {}".format(
                transaction.amount,
                transaction.category,
                transaction.description,
                transaction.created_at
            )
        )

    except IndexError:
        await update.message.reply_text(
            "❌ Wrong command format.\n\n"
            "Use:\n"
            "/income [amount] [category] [description]\n\n"
            "Example:\n"
            "/income 10000 salary scholarship"
        )

    except ValueError:
        await update.message.reply_text(
            "❌ Invalid amount.\n\n"
            "Amount must be a positive number.\n\n"
            "Use:\n"
            "/income [amount] [category] [description]\n\n"
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

        warning = finance_manager.check_spending_limit(
            user_id=update.effective_user.id,
            category=category
        )

        message = (
            "✅ Expense added successfully!\n\n"
            "💸 Amount: {} KZT\n"
            "📂 Category: {}\n"
            "📝 Description: {}\n"
            "📅 Date: {}".format(
                transaction.amount,
                transaction.category,
                transaction.description,
                transaction.created_at
            )
        )

        if warning:
            message += "\n\n⚠️ " + warning

        await update.message.reply_text(message)

    except IndexError:
        await update.message.reply_text(
            "❌ Wrong command format.\n\n"
            "Use:\n"
            "/expense [amount] [category] [description]\n\n"
            "Example:\n"
            "/expense 1500 food lunch"
        )

    except ValueError:
        await update.message.reply_text(
            "❌ Invalid amount.\n\n"
            "Amount must be a positive number.\n\n"
            "Use:\n"
            "/expense [amount] [category] [description]\n\n"
            "Example:\n"
            "/expense 1500 food lunch"
        )


async def balance(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    current_balance = finance_manager.get_balance(user_id)

    await update.message.reply_text(
        "💰 Your current balance\n\n"
        "Balance: {} KZT".format(current_balance)
    )


async def categories(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    summary = finance_manager.get_expense_categories_summary(user_id)

    if not summary:
        await update.message.reply_text("📂 No expense categories found.")
        return

    message = "📂 Expense categories summary:\n\n"

    for category, amount in summary.items():
        message += "• {}: {} KZT\n".format(category, amount)

    await update.message.reply_text(message)


async def search(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text(
            "❌ Wrong command format.\n\n"
            "Use:\n"
            "/search [keyword]\n\n"
            "Example:\n"
            "/search lunch"
        )
        return

    user_id = update.effective_user.id
    keyword = " ".join(context.args)

    results = finance_manager.search_transactions(user_id, keyword)

    if not results:
        await update.message.reply_text("🔎 No transactions found.")
        return

    message = "🔎 Search results for '{}':\n\n".format(keyword)

    for transaction in results:
        sign = "+" if transaction["transaction_type"] == "income" else "-"

        message += "{}{} KZT | {} | {} | {}\n".format(
            sign,
            transaction["amount"],
            transaction["category"],
            transaction["description"],
            transaction["created_at"]
        )

    await update.message.reply_text(message)


async def filter_category(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text(
            "❌ Wrong command format.\n\n"
            "Use:\n"
            "/filter [category]\n\n"
            "Example:\n"
            "/filter food"
        )
        return

    user_id = update.effective_user.id
    category = context.args[0]

    results = finance_manager.filter_by_category(user_id, category)

    if not results:
        await update.message.reply_text("🏷 No transactions found for this category.")
        return

    message = "🏷 Transactions in category '{}':\n\n".format(category)

    for transaction in results:
        sign = "+" if transaction["transaction_type"] == "income" else "-"

        message += "{}{} KZT | {} | {}\n".format(
            sign,
            transaction["amount"],
            transaction["description"],
            transaction["created_at"]
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
            "📊 {} report\n\n"
            "💵 Total income: {} KZT\n"
            "💸 Total expense: {} KZT\n"
            "💰 Balance: {} KZT\n"
            "🔢 Transactions count: {}".format(
                period.capitalize(),
                report_data["total_income"],
                report_data["total_expense"],
                report_data["balance"],
                report_data["transactions_count"]
            )
        )

    except ValueError:
        await update.message.reply_text(
            "❌ Wrong command format.\n\n"
            "Use:\n"
            "/report [week/month]\n\n"
            "Examples:\n"
            "/report week\n"
            "/report month"
        )


async def chart(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    summary = finance_manager.get_expense_categories_summary(user_id)

    if not summary:
        await update.message.reply_text("📈 No expense data for chart.")
        return

    os.makedirs("data/charts", exist_ok=True)

    chart_path = "data/charts/expenses_{}.png".format(user_id)

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


async def limit(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        if len(context.args) < 2:
            raise IndexError

        category = context.args[0]
        amount = float(context.args[1])

        category, amount = finance_manager.set_spending_limit(
            user_id=update.effective_user.id,
            category=category,
            amount=amount
        )

        await update.message.reply_text(
            "✅ Spending limit set successfully!\n\n"
            "📂 Category: {}\n"
            "⚠️ Limit: {} KZT".format(category, amount)
        )

    except IndexError:
        await update.message.reply_text(
            "❌ Wrong command format.\n\n"
            "Use:\n"
            "/limit [category] [amount]\n\n"
            "Example:\n"
            "/limit food 5000"
        )

    except ValueError:
        await update.message.reply_text(
            "❌ Invalid limit amount.\n\n"
            "Amount must be a positive number.\n\n"
            "Use:\n"
            "/limit [category] [amount]\n\n"
            "Example:\n"
            "/limit food 5000"
        )


async def limits(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user_limits = finance_manager.get_spending_limits(user_id)

    if not user_limits:
        await update.message.reply_text("📌 No spending limits found.")
        return

    message = "📌 Your spending limits:\n\n"

    for category, amount in user_limits.items():
        message += "• {}: {} KZT\n".format(category, amount)

    await update.message.reply_text(message)


async def regex_search(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        if not context.args:
            raise IndexError

        pattern = " ".join(context.args)
        user_id = update.effective_user.id

        results = finance_manager.regex_search_transactions(user_id, pattern)

        if not results:
            await update.message.reply_text("🧩 No transactions found.")
            return

        message = "🧩 Regex search results for '{}':\n\n".format(pattern)

        for transaction in results:
            sign = "+" if transaction["transaction_type"] == "income" else "-"

            message += "{}{} KZT | {} | {} | {}\n".format(
                sign,
                transaction["amount"],
                transaction["category"],
                transaction["description"],
                transaction["created_at"]
            )

        await update.message.reply_text(message)

    except IndexError:
        await update.message.reply_text(
            "❌ Wrong command format.\n\n"
            "Use:\n"
            "/regex [pattern]\n\n"
            "Example:\n"
            "/regex lunch|coffee"
        )

    except ValueError:
        await update.message.reply_text(
            "❌ Invalid regex pattern.\n\n"
            "Use:\n"
            "/regex [pattern]\n\n"
            "Example:\n"
            "/regex lunch|coffee"
        )


async def export(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        user_id = update.effective_user.id
        file_path = finance_manager.export_to_csv(user_id)

        await update.message.reply_text("📤 CSV export created successfully!")

        with open(file_path, "rb") as document:
            await update.message.reply_document(document=document)

    except ValueError:
        await update.message.reply_text("📤 No transactions to export.")


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
    app.add_handler(CommandHandler("limit", limit))
    app.add_handler(CommandHandler("limits", limits))
    app.add_handler(CommandHandler("regex", regex_search))
    app.add_handler(CommandHandler("export", export))

    print("Smart Finance Bot is running...")
    app.run_polling()


if __name__ == "__main__":
    main()