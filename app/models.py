from datetime import datetime


class Transaction:
    def __init__(self, user_id, amount, category, description, transaction_type, created_at):
        self.user_id = user_id
        self.amount = amount
        self.category = category
        self.description = description
        self.transaction_type = transaction_type
        self.created_at = created_at

    @classmethod
    def create(cls, user_id, amount, category, description, transaction_type):
        created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        return cls(
            user_id=user_id,
            amount=amount,
            category=category,
            description=description,
            transaction_type=transaction_type,
            created_at=created_at
        )

    def to_dict(self):
        return {
            "user_id": self.user_id,
            "amount": self.amount,
            "category": self.category,
            "description": self.description,
            "transaction_type": self.transaction_type,
            "created_at": self.created_at
        }


class User:
    def __init__(self, user_id, username=None):
        self.user_id = user_id
        self.username = username


class Category:
    def __init__(self, name):
        self.name = name