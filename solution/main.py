from solution.finance_tracker import FinanceTracker, ensure_files_directory_exists
from solution.transaction import Transaction
import os


def add_transaction_ui(tracker):
    """Функция для добавления транзакции (взаимодействие с пользователем)."""
    amount = float(input("Введите сумму: "))
    category = input("Введите категорию: ").strip()
    date = input("Введите дату (ГГГГ-ММ-ДД): ")
    transaction_type = input("Введите тип (income/expense): ").strip().lower()
    transaction = Transaction(amount, category, date, transaction_type)
    tracker.add_transaction(transaction)
    print("Транзакция добавлена!")


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
        print("6. Выйти")
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
            print("Выход из программы")
            break
        else:
            print("Неверный выбор. Попробуйте снова.")


if __name__ == "__main__":
    main()
