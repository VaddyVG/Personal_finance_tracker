from solution.finance_tracker import FinanceTracker, ensure_files_directory_exists
from solution.transaction import Transaction
from prompt_toolkit import prompt
from solution.validation import AmountValidator, DateValidator, type_completer
import os


def add_transaction_ui(tracker):
    """Функция для добавления транзакции (взаимодействие с пользователем)."""
    try:
        amount = float(prompt("Введите сумму: ", validator=AmountValidator()))
        category = prompt("Введите категорию: ").strip()
        if not category:
            print("Ошибка: Категория не может быть пустой.")
            return

        date = prompt("Введите дату (ГГГГ-ММ-ДД): ", validator=DateValidator())
        transaction_type = prompt(
            "Введите тип (income/expense): ",
            completer=type_completer,
            complete_while_typing=True
        ).lower()

        if transaction_type not in ("income", "expense"):
            print("Ошибка: Тип должен быть 'income' или 'expense'.")
            return

        transaction = Transaction(amount, category, date, transaction_type)
        tracker.add_transaction(transaction)
        print("Транзакция добавлена!")
    except KeyboardInterrupt:
        print("\nОтменено пользователем.")
    except Exception as e:
        print(f"Неожиданная ошибка: {e}")


def edit_transaction_ui(tracker):
    """Интерфейс для редактирования транзакции."""
    try:
        index = int(prompt("Введите индекс транзакции для редактирования: "))
        if not (0 <= index < len(tracker.transactions)):
            print("Неверный индекс транзакции.")
            return

        amount = float(prompt("Введите новую сумму: ", validator=AmountValidator()))
        category = prompt("Введите новую категорию: ").strip()
        if not category:
            print("Ошибка: категория не может быть пустой.")
            return

        date = prompt("Введите новую дату (ГГГГ-ММ-ДД): ", validator=DateValidator())
        transaction_type = prompt(
            "Введите новый тип (income/expense): ",
            completer=type_completer,
            complete_while_typing=True
        ).lower()
        if transaction_type not in ("income", "expense"):
            print("Ошибка: Тип должен быть 'income' или 'expense'.")
            return

        filename = prompt("Введите имя файла для изменения (например, data.csv): ").strip()
        if not filename:
            print("Ошибка: Имя файла не может быть пустым.")
            return

        new_transaction = Transaction(amount, category, date, transaction_type)
        tracker.edit_transaction(index, new_transaction, filename)
        print("Транзакция успешно отредактирована!")
    except KeyboardInterrupt:
        print("\nОтменено пользователем.")
    except Exception as e:
        print(f"Неожиданная ошибка: {e}")


def delete_transaction_ui(tracker):
    """Интерфейс для удаления транзакции."""
    try:
        index = int(prompt("Введите индекс транзакции для удаления: "))
        if not (0 <= index < len(tracker.transactions)):
            print("Неверный индекс транзакции.")
            return

        filename = prompt("Введите имя файла для удаления (например, data.csv): ").strip()
        if not filename:
            print("Ошибка: Имя файла не может быть пустым.")
            return

        tracker.delete_transaction(index, filename)
        print("Транзакция успешно удалена!")
    except KeyboardInterrupt:
        print("\nОтменено пользователем.")
    except Exception as e:
        print(f"Неожиданная ошибка: {e}")


def show_balance_ui(tracker):
    """Функция для показа текущего баланса."""
    balance = tracker.get_balance()
    print(f"Ваш текущий баланс: {balance} руб.")


def show_monthly_report_ui(tracker):
    """Функция для показа отчета за месяц."""
    try:
        month = int(prompt("Введите месяц (1-12): "))
        year = int(prompt("Введите год: "))
        report = tracker.get_monthly_report(month, year)
        if report:
            for t in report:
                print(t)
        else:
            print("Нет транзакций за указанный период.")
    except ValueError:
        print("Ошибка: Введите корректные числовые значения для месяца и года.")
    except Exception as e:
        print(f"Неожиданная ошибка: {e}")


def plot_spending_ui(tracker):
    """Функция для визуализации расходов по категориям."""
    tracker.plot_spending_by_category()


def export_to_csv_ui(tracker):
    """Функция для экспорта данных в CSV."""
    try:
        filename = prompt("Введите имя файла для экспорта (например, data.csv): ").strip()
        if not filename:
            print("Ошибка: Имя файла не может быть пустым.")
            return

        filepath = os.path.join("files", filename)
        if os.path.exists(filepath):
            choice = prompt("Файл уже существует. Добавить данные? (y/n): ").strip().lower()
            mode = "a" if choice == "y" else "w"
        else:
            mode = "w"

        tracker.export_to_csv(filename, mode)
        print("Данные успешно экспортированы.")
    except KeyboardInterrupt:
        print("\nОтменено пользователем.")
    except Exception as e:
        print(f"Неожиданная ошибка: {e}")


def select_csv_file():
    """Показывает список CSV-файлов в директории files и позволяет выбрать один."""
    ensure_files_directory_exists()
    csv_files = [f for f in os.listdir("files") if f.endswith(".csv")]

    if not csv_files:
        print("CSV-файлы не найдены. Начинаем с пустого списка.")
        return None

    print("Доступные CSV-файлы:")
    for i, filename in enumerate(csv_files, start=1):
        print(f"{i}. {filename}")

    choice = prompt("Выберите номер файла (или Enter, чтобы начать с пустого списка): ").strip()
    if choice.isdigit() and 1 <= int(choice) <= len(csv_files):
        return csv_files[int(choice) - 1]
    else:
        print("Загрузка данных отменена.")
        return None


def main():
    tracker = FinanceTracker()
    selected_file = select_csv_file()
    if selected_file:
        tracker.load_from_csv(selected_file)

    while True:
        print("\n=== Личный финансовый трекер ===")
        print("1. Добавить транзакцию")
        print("2. Показать баланс")
        print("3. Показать отчет за месяц")
        print("4. Визуализировать расходы")
        print("5. Экспорт в CSV")
        print("6. Редактировать транзакцию")
        print("7. Удалить транзакцию")
        print("8. Выйти")

        choice = prompt("Выберите действие: ").strip()
        if choice == "1":
            add_transaction_ui(tracker)
        elif choice == "2":
            show_balance_ui(tracker)
        elif choice == "3":
            show_monthly_report_ui(tracker)
        elif choice == "4":
            plot_spending_ui(tracker)
        elif choice == "5":
            export_to_csv_ui(tracker)
        elif choice == "6":
            edit_transaction_ui(tracker)
        elif choice == "7":
            delete_transaction_ui(tracker)
        elif choice == "8":
            print("Выход из программы.")
            break
        else:
            print("Неверный выбор. Попробуйте снова.")
