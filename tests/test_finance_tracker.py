import os
import csv
from solution.finance_tracker import FinanceTracker
from solution.transaction import Transaction


def test_add_transaction():
    """Проверяет добавление транзакции."""
    tracker = FinanceTracker()
    transaction = Transaction(100, "Еда", "2023-10-01", "expense")
    tracker.add_transaction(transaction)
    assert len(tracker.transactions) == 1
    assert tracker.transactions[0] == transaction


def test_get_balance():
    """Проверяет расчет баланса."""
    tracker = FinanceTracker()
    tracker.add_transaction(Transaction(50000, "Зарплата", "2023-10-01", "income"))
    tracker.add_transaction(Transaction(1500, "Еда", "2023-10-02", "expense"))
    assert tracker.get_balance() == 48500


def test_export_to_csv(tmpdir):
    """Проверяет экспорт транзакций в CSV-файл."""
    tracker = FinanceTracker()
    tracker.add_transaction(Transaction(100, "Еда", "2023-10-01", "expense"))
    tracker.add_transaction(Transaction(50000, "Зарплата", "2023-10-01", "income"))
    filename = tmpdir.join("test_data.csv")  # Используем временную директорию
    tracker.export_to_csv(filename, mode="w")

    # Проверяем, что файл создан и содержит правильные данные
    assert os.path.exists(filename)
    with open(filename, mode="r", encoding="utf-8") as file:
        reader = csv.reader(file)
        rows = list(reader)
        assert rows[0] == ["Date", "Type", "Category", "Amount"]
        assert rows[1] == ["2023-10-01", "expense", "Еда", "100"]
        assert rows[2] == ["2023-10-01", "income", "Зарплата", "50000"]


def test_load_from_csv(tmpdir):
    """Проверяет загрузку транзакций из CSV-файла."""
    filename = tmpdir.join("test_data.csv")
    with open(filename, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["Date", "Type", "Category", "Amount"])
        writer.writerow(["2023-10-01", "expense", "Еда", "100"])
        writer.writerow(["2023-10-01", "income", "Зарплата", "50000"])
    
    # Загружаем данные из файла
    tracker = FinanceTracker()
    tracker.load_from_csv(filename)

    # Проверяем, что данные загружены корректно
    assert len(tracker.transactions) == 2
    assert tracker.transactions[0].amount == 100
    assert tracker.transactions[0].category == "Еда"
    assert tracker.transactions[1].amount == 50000
    assert tracker.transactions[1].category == "Зарплата"
