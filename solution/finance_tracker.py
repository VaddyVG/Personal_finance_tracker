import csv
import os
import matplotlib.pyplot as plt
from solution.transaction import Transaction


def ensure_files_directory_exists():
    """Создает папку files если ее еще нет."""
    if not os.path.exists("files"):
        os.makedirs("files")

class FinanceTracker:
    """Класс для управления финансами."""
    def __init__(self):
        self.transactions = []  # Список для хранения всех транзакций
    
    def add_transaction(self, transaction):
        """Добавление новой транзакции в список."""
        self.transactions.append(transaction)

    def edit_transaction(self, index, new_transaction, filename="data.csv"):
        """
        Редактирует транзакцию по индексу.
        :param index: Индекс транзакции.
        :param new_transaction: Новая транзакция.
        """
        if 0 <= index < len(self.transactions):
            self.transactions[index] = new_transaction
            self.export_to_csv(filename)
    
    def delete_transaction(self, index, filename="data.csv"):
        """
        Удаляет транзакцию по индексу
        :param index: Индекс транзакции
        """
        if 0 <= index < len(self.transactions):
            self.transactions.pop(index)
            self.export_to_csv(filename)
    
    def get_balance(self):
        """Расчет текущего баланса (доходы минус расходы)."""
        income = sum(t.amount for t in self.transactions if t.type == "income")
        expense = sum(t.amount for t in self.transactions if t.type == "expense")
        return income - expense

    def get_transactions_by_category(self, category):
        """Получение всех транзакций по указанной категории."""
        return [t for t in self.transactions if t.category == category]

    def get_monthly_report(self, month, year):
        """Получение всех транзакций за указанный месяц и год."""
        monthly_transactions = [
            t for t in self.transactions
            if t.date.month == month and t.date.year == year
        ]
        return monthly_transactions

    def export_to_csv(self, filename, mode="w"):
        """
        Экспортирует транзакции в CSV-файл.
        :param filename: Имя файла.
        :param mode: Режим записи ("w" для перезаписи, "a" для добавления).
        """
        ensure_files_directory_exists()
        filepath = os.path.join("files", filename)  # Полный путь к файлу
        try:
            with open(filepath, mode=mode, newline="", encoding="utf-8") as file:
                self._writer_header(file, mode)
                new_transactions = self._get_new_transaction(filepath, mode)
                self._write_transactions(file, new_transactions)
            print(f"Данные успешно экспортированы в {filepath}.")
        except Exception as e:
            print(f"Ошибка при экспорте данных: {e}")

    def _writer_header(self, file, mode):
        """
        Записывает заголовок CSV-файла, если файл открыт в режиме перезаписи
        """
        if mode == "w":
            writer = csv.writer(file)
            writer.writerow(["Date", "Type", "Category", "Amount"])

    def _get_new_transaction(self, filename, mode):
        """
        Возвращает список новых транзакций, которые еще не записаны в файл.
        """
        if mode == "a":
            existing_transactions = self._load_existing_transactions(filename)
            # Используем множества для поиска новых транзакций
            existing_set = set(existing_transactions)
            current_set = set(self.transactions)
            new_transactions = list(current_set - existing_set)
            return new_transactions
        return self.transactions

    def _write_transactions(self, file, transactions):
        """
        Записывает транзакции в CSV-файл.
        """
        writer = csv.writer(file)
        for t in transactions:
            writer.writerow([t.date.strftime("%Y-%m-%d"), t.type, t.category, t.amount])

    def _load_existing_transactions(self, filename):
        """
        Загружает существующие транзакции из CSV-файла.
        """
        existing_transactions = []
        try:
            with open(filename, mode="r", encoding="utf-8") as file:
                reader = csv.DictReader(file)
                for row in reader:
                    amount = float(row["Amount"])
                    category = row["Category"]
                    date = row["Date"]
                    transaction_type = row["Type"]
                    transaction = Transaction(amount, category, date, transaction_type)
                    existing_transactions.append(transaction)
        except Exception as e:
            print(f"Ошибка при загрузке существующих транзакций: {e}")
        return existing_transactions

    def load_from_csv(self, filename):
        """Загружает тразакции из csv."""
        ensure_files_directory_exists()  # Убедимся, что папка 'files' существует
        filepath = os.path.join("files", filename)  # Полный путь к файлу
        try:
            self.transactions = []
            with open(filepath, "r", encoding="utf-8") as my_file:
                reader = csv.DictReader(my_file)
                for row in reader:
                    amount = float(row["Amount"])
                    category = row["Category"]
                    date = row["Date"]
                    transaction_type = row["Type"]
                    transaction = Transaction(amount, category, date, transaction_type)
                    self.add_transaction(transaction)
            print(f"Данные успешно загружены из {filepath}")
        except FileNotFoundError:
            print(f"Файл {filepath} не найден. Начните с пустого списка транзакций.")
        except Exception as e:
            print(f"Ошибка при загрузке данных: {e}")

    def plot_spending_by_category(self):
        """Визуализация расходов по категориям в виде круговой диаграммы."""
        categories = {}
        for t in self.transactions:
            if t.type == "expense":
                categories[t.category] = categories.get(t.category, 0) + t.amount

        plt.figure(figsize=(8, 8))
        plt.pie(categories.values(), labels=categories.keys(), autopct="%1.1f%%", startangle=140)
        plt.title("Распределение расходов по категориям")
        plt.show()
