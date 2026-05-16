import os
import tempfile
import unittest

from app.finance import FinanceManager
from app.storage import JsonStorage


class TestFinanceManager(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.test_file = os.path.join(self.temp_dir.name, "test_users.json")

        self.manager = FinanceManager()
        self.manager.storage = JsonStorage(self.test_file)

        self.user_id = 12345

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_add_income(self):
        transaction = self.manager.add_transaction(
            user_id=self.user_id,
            amount=10000,
            category="salary",
            description="scholarship",
            transaction_type="income"
        )

        self.assertEqual(transaction.amount, 10000)
        self.assertEqual(transaction.category, "salary")
        self.assertEqual(transaction.description, "scholarship")
        self.assertEqual(transaction.transaction_type, "income")

    def test_add_expense(self):
        transaction = self.manager.add_transaction(
            user_id=self.user_id,
            amount=1500,
            category="food",
            description="lunch",
            transaction_type="expense"
        )

        self.assertEqual(transaction.amount, 1500)
        self.assertEqual(transaction.category, "food")
        self.assertEqual(transaction.description, "lunch")
        self.assertEqual(transaction.transaction_type, "expense")

    def test_balance(self):
        self.manager.add_transaction(
            self.user_id,
            10000,
            "salary",
            "scholarship",
            "income"
        )

        self.manager.add_transaction(
            self.user_id,
            1500,
            "food",
            "lunch",
            "expense"
        )

        balance = self.manager.get_balance(self.user_id)

        self.assertEqual(balance, 8500)

    def test_expense_categories_summary(self):
        self.manager.add_transaction(
            self.user_id,
            1500,
            "food",
            "lunch",
            "expense"
        )

        self.manager.add_transaction(
            self.user_id,
            500,
            "food",
            "coffee",
            "expense"
        )

        self.manager.add_transaction(
            self.user_id,
            1000,
            "transport",
            "taxi",
            "expense"
        )

        summary = self.manager.get_expense_categories_summary(self.user_id)

        self.assertEqual(summary["food"], 2000)
        self.assertEqual(summary["transport"], 1000)

    def test_search_transactions(self):
        self.manager.add_transaction(
            self.user_id,
            1500,
            "food",
            "lunch",
            "expense"
        )

        results = self.manager.search_transactions(self.user_id, "lunch")

        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["description"], "lunch")

    def test_filter_by_category(self):
        self.manager.add_transaction(
            self.user_id,
            1500,
            "food",
            "lunch",
            "expense"
        )

        self.manager.add_transaction(
            self.user_id,
            1000,
            "transport",
            "bus",
            "expense"
        )

        results = self.manager.filter_by_category(self.user_id, "food")

        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["category"], "food")

    def test_report_week(self):
        self.manager.add_transaction(
            self.user_id,
            10000,
            "salary",
            "scholarship",
            "income"
        )

        self.manager.add_transaction(
            self.user_id,
            1500,
            "food",
            "lunch",
            "expense"
        )

        report = self.manager.get_report(self.user_id, "week")

        self.assertEqual(report["total_income"], 10000)
        self.assertEqual(report["total_expense"], 1500)
        self.assertEqual(report["balance"], 8500)
        self.assertEqual(report["transactions_count"], 2)

    def test_spending_limit(self):
        self.manager.set_spending_limit(
            self.user_id,
            "food",
            5000
        )

        limits = self.manager.get_spending_limits(self.user_id)

        self.assertEqual(limits["food"], 5000)

    def test_spending_limit_warning(self):
        self.manager.set_spending_limit(
            self.user_id,
            "food",
            5000
        )

        self.manager.add_transaction(
            self.user_id,
            4500,
            "food",
            "dinner",
            "expense"
        )

        warning = self.manager.check_spending_limit(self.user_id, "food")

        self.assertIsNotNone(warning)
        self.assertIn("80%", warning)

    def test_regex_search(self):
        self.manager.add_transaction(
            self.user_id,
            1500,
            "food",
            "lunch",
            "expense"
        )

        self.manager.add_transaction(
            self.user_id,
            800,
            "transport",
            "bus",
            "expense"
        )

        results = self.manager.regex_search_transactions(
            self.user_id,
            "lunch|bus"
        )

        self.assertEqual(len(results), 2)

    def test_invalid_amount(self):
        with self.assertRaises(ValueError):
            self.manager.add_transaction(
                self.user_id,
                -100,
                "food",
                "wrong amount",
                "expense"
            )

    def test_invalid_regex(self):
        with self.assertRaises(ValueError):
            self.manager.regex_search_transactions(
                self.user_id,
                "[invalid"
            )

    def test_export_to_csv(self):
        self.manager.add_transaction(
            self.user_id,
            10000,
            "salary",
            "scholarship",
            "income"
        )

        file_path = self.manager.export_to_csv(self.user_id)

        self.assertTrue(os.path.exists(file_path))
        self.assertTrue(file_path.endswith(".csv"))


if __name__ == "__main__":
    unittest.main()