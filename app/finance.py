import csv
import os
import re
from datetime import datetime, timedelta
from collections import defaultdict

from app.models import Transaction
from app.storage import JsonStorage


class FinanceManager:
    def __init__(self):
        self.storage = JsonStorage()

    def add_transaction(
        self,
        user_id: int,
        amount: float,
        category: str,
        description: str,
        transaction_type: str,
    ):
        if amount <= 0:
            raise ValueError("Amount must be greater than zero.")

        if not category:
            raise ValueError("Category cannot be empty.")

        if transaction_type not in ["income", "expense"]:
            raise ValueError("Transaction type must be income or expense.")

        data = self.storage.load_data()
        user_key = str(user_id)

        if user_key not in data:
            data[user_key] = {
                "transactions": [],
                "limits": {}
            }

        if "transactions" not in data[user_key]:
            data[user_key]["transactions"] = []

        if "limits" not in data[user_key]:
            data[user_key]["limits"] = {}

        transaction = Transaction.create(
            user_id=user_id,
            amount=amount,
            category=category.lower(),
            description=description,
            transaction_type=transaction_type,
        )

        data[user_key]["transactions"].append(transaction.to_dict())
        self.storage.save_data(data)

        return transaction

    def get_transactions(self, user_id: int) -> list:
        data = self.storage.load_data()
        user_key = str(user_id)

        if user_key not in data:
            return []

        return data[user_key].get("transactions", [])

    def get_balance(self, user_id: int) -> float:
        transactions = self.get_transactions(user_id)
        balance = 0.0

        for transaction in transactions:
            amount = float(transaction["amount"])

            if transaction["transaction_type"] == "income":
                balance += amount
            elif transaction["transaction_type"] == "expense":
                balance -= amount

        return balance

    def get_expense_categories_summary(self, user_id: int) -> dict:
        transactions = self.get_transactions(user_id)
        categories = defaultdict(float)

        for transaction in transactions:
            if transaction["transaction_type"] == "expense":
                category = transaction["category"]
                amount = float(transaction["amount"])
                categories[category] += amount

        return dict(categories)

    def search_transactions(self, user_id: int, keyword: str) -> list:
        transactions = self.get_transactions(user_id)
        keyword = keyword.lower()
        results = []

        for transaction in transactions:
            category = transaction["category"].lower()
            description = transaction["description"].lower()

            if keyword in category or keyword in description:
                results.append(transaction)

        return results

    def filter_by_category(self, user_id: int, category: str) -> list:
        transactions = self.get_transactions(user_id)
        category = category.lower()

        return [
            transaction
            for transaction in transactions
            if transaction["category"].lower() == category
        ]

    def get_report(self, user_id: int, period: str) -> dict:
        transactions = self.get_transactions(user_id)
        now = datetime.now()

        if period == "week":
            start_date = now - timedelta(days=7)
        elif period == "month":
            start_date = now - timedelta(days=30)
        else:
            raise ValueError("Period must be 'week' or 'month'.")

        total_income = 0.0
        total_expense = 0.0
        count = 0

        for transaction in transactions:
            transaction_date = datetime.strptime(
                transaction["created_at"],
                "%Y-%m-%d %H:%M:%S"
            )

            if transaction_date >= start_date:
                count += 1

                if transaction["transaction_type"] == "income":
                    total_income += float(transaction["amount"])
                elif transaction["transaction_type"] == "expense":
                    total_expense += float(transaction["amount"])

        return {
            "period": period,
            "total_income": total_income,
            "total_expense": total_expense,
            "balance": total_income - total_expense,
            "transactions_count": count,
        }

    def set_spending_limit(self, user_id: int, category: str, amount: float):
        if amount <= 0:
            raise ValueError("Limit amount must be greater than zero.")

        if not category:
            raise ValueError("Category cannot be empty.")

        data = self.storage.load_data()
        user_key = str(user_id)

        if user_key not in data:
            data[user_key] = {
                "transactions": [],
                "limits": {}
            }

        if "limits" not in data[user_key]:
            data[user_key]["limits"] = {}

        data[user_key]["limits"][category.lower()] = amount
        self.storage.save_data(data)

        return category.lower(), amount

    def get_spending_limits(self, user_id: int) -> dict:
        data = self.storage.load_data()
        user_key = str(user_id)

        if user_key not in data:
            return {}

        return data[user_key].get("limits", {})

    def check_spending_limit(self, user_id: int, category: str):
        limits = self.get_spending_limits(user_id)
        category = category.lower()

        if category not in limits:
            return None

        summary = self.get_expense_categories_summary(user_id)
        spent = summary.get(category, 0)
        limit = limits[category]

        if spent >= limit:
            return "Warning: you reached the limit for category '{}'. Spent: {}, Limit: {}".format(
                category,
                spent,
                limit
            )

        if spent >= limit * 0.8:
            return "Warning: you spent more than 80% of limit for category '{}'. Spent: {}, Limit: {}".format(
                category,
                spent,
                limit
            )

        return None

    def regex_search_transactions(self, user_id: int, pattern: str) -> list:
        transactions = self.get_transactions(user_id)
        results = []

        try:
            regex = re.compile(pattern, re.IGNORECASE)
        except re.error:
            raise ValueError("Invalid regex pattern.")

        for transaction in transactions:
            text = "{} {} {}".format(
                transaction["category"],
                transaction["description"],
                transaction["transaction_type"]
            )

            if regex.search(text):
                results.append(transaction)

        return results

    def get_short_user_id(self, user_id: int) -> int:
        data = self.storage.load_data()
        user_keys = list(data.keys())

        user_key = str(user_id)

        if user_key not in user_keys:
            return len(user_keys) + 1

        return user_keys.index(user_key) + 1

    def export_to_csv(self, user_id: int) -> str:
        transactions = self.get_transactions(user_id)

        if not transactions:
            raise ValueError("No transactions to export.")

        os.makedirs("data/exports", exist_ok=True)

        file_path = "data/exports/transactions_{}.csv".format(user_id)

        with open(file_path, "w", newline="", encoding="utf-8-sig") as file:
            writer = csv.writer(file, delimiter=";")

            writer.writerow([
                "user_number",
                "amount",
                "category",
                "description",
                "transaction_type",
                "created_at"
            ])

            for transaction in transactions:
                writer.writerow([
                    self.get_short_user_id(transaction["user_id"]),
                    transaction["amount"],
                    transaction["category"],
                    transaction["description"],
                    transaction["transaction_type"],
                    transaction["created_at"]
                ])

        return file_path