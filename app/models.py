from dataclasses import dataclass
from datetime import datetime


@dataclass
class Transaction:
    user_id: int
    amount: float
    category: str
    description: str
    transaction_type: str
    created_at: str

    def to_dict(self) -> dict:
        return {
            "user_id": self.user_id,
            "amount": self.amount,
            "category": self.category,
            "description": self.description,
            "transaction_type": self.transaction_type,
            "created_at": self.created_at,
        }

    @staticmethod
    def create(user_id: int, amount: float, category: str, description: str, transaction_type: str):
        return Transaction(
            user_id=user_id,
            amount=amount,
            category=category,
            description=description,
            transaction_type=transaction_type,
            created_at=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        )


@dataclass
class User:
    user_id: int
    username: str | None = None


@dataclass
class Category:
    name: str