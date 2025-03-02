import os
import csv
from datetime import datetime
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


def test_edit_transaction():
    """Проверяет редактирование транзакции по индексу."""
    tracker = FinanceTracker()
    transaction1 = Transaction(100, "Еда", "2023-10-01", "expense")
    transaction2 = Transaction(50000, "Зарплата", "2023-10-01", "income")
    tracker.add_transaction(transaction1)
    tracker.add_transaction(transaction2)

    # Редактируем первую транзакцию
    new_transaction = Transaction(200, "Транспорт", "2023-10-02", "expense")
    tracker.edit_transaction(0, new_transaction)

    # Проверяем, что транзакция изменилась
    assert len(tracker.transactions) == 2
    assert tracker.transactions[0].amount == 200
    assert tracker.transactions[0].category == "Транспорт"
    assert tracker.transactions[0].date == datetime.strptime("2023-10-02", "%Y-%m-%d")
    assert tracker.transactions[0].type == "expense"


def test_edit_transaction_invalid_index():
    """Проверяет обработку неверного индекса при редактировании"""
    tracker = FinanceTracker()
    transaction = Transaction(100, "Еда", "2023-10-01", "expense")
    tracker.add_transaction(transaction)

    # Пытаемся редактировать несуществующую транзакцию
    new_transaction = Transaction(200, "Транспорт", "2023-10-02", "expense")
    tracker.edit_transaction(1, new_transaction)

    # Проверяем, что транзакция не изменилась
    assert len(tracker.transactions) == 1
    assert tracker.transactions[0].amount == 100
    assert tracker.transactions[0].category == "Еда"


def test_delete_transaction():
    """Проверяет удаление транзакции по индексу."""
    tracker = FinanceTracker()
    transaction1 = Transaction(100, "Еда", "2023-10-01", "expense")
    transaction2 = Transaction(50000, "Зарплата", "2023-10-01", "income")
    tracker.add_transaction(transaction1)
    tracker.add_transaction(transaction2)

    # Удаляем первую транзакцию
    tracker.delete_transaction(0)
    # Проверяем, что транзакция удалена
    assert len(tracker.transactions) == 1
    assert tracker.transactions[0].amount == 50000
    assert tracker.transactions[0].category == "Зарплата"


def test_delete_transaction_invalid_index():
    """Проверяет обработку неверного индекса при удалении."""
    tracker = FinanceTracker()
    transaction = Transaction(100, "Еда", "2023-10-01", "expense")
    tracker.add_transaction(transaction)

    # Пытаемся удалить несуществующую транзакцию
    tracker.delete_transaction(1)  # Неверный индекс

    # Проверяем, что транзакция не удалена
    assert len(tracker.transactions) == 1
    assert tracker.transactions[0].amount == 100
    assert tracker.transactions[0].category == "Еда"
