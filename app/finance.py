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
        data = self.storage.load_data()
        user_key = str(user_id)

        if user_key not in data:
            data[user_key] = {
                "transactions": []
            }

        transaction = Transaction.create(
            user_id=user_id,
            amount=amount,
            category=category,
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

        return data[user_key]["transactions"]

    def get_balance(self, user_id: int) -> float:
        transactions = self.get_transactions(user_id)
        balance = 0

        for transaction in transactions:
            if transaction["transaction_type"] == "income":
                balance += transaction["amount"]
            elif transaction["transaction_type"] == "expense":
                balance -= transaction["amount"]

        return balance