from solution.finance_tracker import FinanceTracker, ensure_files_directory_exists
from solution.transaction import Transaction
from prompt_toolkit import prompt
from solution.validation import AmountValidator, DateValidator, type_completer
import os


def add_transaction_ui(tracker):
    """Функция для добавления транзакции (взаимодействие с пользователем)."""
    try:
        amount = float(prompt(
            "Введите сумму: ",
            validator=AmountValidator()
        ))
        category = prompt("Введите категорию: ").strip()
        if not category:
            print("Ошибка: Категория не может быть пустой.")
            return

        date = prompt(
            "Введите дату (ГГГГ-ММ-ДД): ",
            validator=DateValidator()
        )

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
        amount = float(prompt(
            "Введите новую сумму: ",
            validator=AmountValidator()
        ))

        category = prompt("Введите новую категорию: ").strip()
        if not category:
            print("Ошибка: категория не может быть пустой.")
            return
        
        date = prompt(
            "Введите новую дату (ГГГГ-ММ-ДД): ",
            validator=DateValidator()
        )

        transaction_type = prompt(
            "Введите новый тип (income/expense): ",
            completer=type_completer,
            complete_while_typing=True
        ).lower()

        if transaction_type not in ("income", "expense"):
            print("Ошибка: Тип должен быть 'income' или 'expense'.")
            return

        new_transaction = Transaction(amount, category, date, transaction_type)
        filename = prompt("Введите имя файла для изменения (например, data.csv): ").strip()
        if not filename:
            print("Ошибка: Имя файла не может быть пустым.")
            return
        
        tracker.edit_transaction(index, new_transaction, filename)
        print("Транзакция успешно отредактирована!")
    except KeyboardInterrupt:
        print("\nОтменено пользователем.")
    except Exception as e:
        print(f"Неожиданная ошибка: {e}")


def delete_transaction_ui(tracker):
    """Интерфейс для удаления транзакции."""
    index = int(input("Введите индекс транзакции для удаления: "))
    if 0 <= index < len(tracker.transactions):
        filename = input("Введите имя файла для удаления (например, data.csv): ")
        tracker.delete_transaction(index, filename)
        print("Транзакция успешно удалена!")
    else:
        print("Неверный индекс транзакции.")


def show_balance_ui(tracker):
    """Функция для показа текущего баланса."""
    balance = tracker.get_balance()
    print(f"Ваш текущий баланс: {balance} руб.")


def show_monthly_report_ui(tracker):
    """Функция для показа отчета за месяц."""
    month = int(input("Введите месяц (1-12): "))
    year = int(input("Введите год: "))
    report = tracker.get_monthly_report(month, year)
    for t in report:
        print(t)


def plot_spending_ui(tracker):
    """Функция для визуализации расходов по категориям."""
    tracker.plot_spending_by_category()


def export_to_csv_ui(tracker):
    """Функция для экспорта данных в CSV."""
    filename = input("Введите имя файла для экспорта (например, data.csv): ")
    filepath = os.path.join("files", filename)
    if os.path.exists(filepath):
        choice = input("Файл уже существует. Добавить данные? (y/n): ").lower()
        mode = "a" if choice == "y" else "w"
    else:
        mode = "w"
    tracker.export_to_csv(filename, mode)


def select_csv_file():
    """
    Показывает список CSV-файлов в текущей 
    директории и позволяет выбрать один.
    """
    ensure_files_directory_exists()
    csv_files = [f for f in os.listdir("files") if f.endswith(".csv")]
    if not csv_files:
        print("CSV-файлы не найдены в текущей директории.")
        return None
    
    print("Доступные CSV-файлы:")
    for i, filename in enumerate(csv_files, start=1):
        print(f"{i}. {filename}")
    
    choice = input("Выберите номер файла для загрузки (или нажмите Enter, чтобы начать с пустого списка): ")
    if choice.isdigit() and 1 <= int(choice) <= len(csv_files):
        return csv_files[int(choice) - 1]
    else:
        print("Загрузка данных отменена. Начинаем с пустого списка.")
        return None


def main():
    tracker = FinanceTracker()  # Создаем объект для учета финансов

    # Предлагаем пользователю выбрать CSV-файл для загрузки
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
        choice = input("Выберите действие: ")
    
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
