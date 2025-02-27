from solution.transaction import Transaction
from datetime import datetime


def test_transaction_creation():
    """Проверяет, что транзакция создаётся корректно."""
    transaction = Transaction(100, "Еда", "2023-10-01", "expense")
    assert transaction.amount == 100
    assert transaction.category == "Еда"
    assert transaction.date == datetime.strptime("2023-10-01", "%Y-%m-%d")


def test_transaction_str():
    """Проверяет строковое представление транзакции."""
    transaction = Transaction(100, "Еда", "2023-10-01", "expense")
    expected_str = "2023-10-01 | EXPENSE | Еда: 100 руб."
    assert str(transaction) == expected_str
