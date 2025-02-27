from datetime import datetime


class Transaction:
    """Класс для представления транзакции."""
    def __init__(self, amount, category, date, transaction_type):
        self.amount = amount  # Сумма транзакции
        self.category = category  # Категория транзакции (например, "Еда", "Транспорт")
        self.date = datetime.strptime(date, "%Y-%m-%d")  # Дата в формате ГГГГ-ММ-ДД
        self.type = transaction_type  # Тип: "income" (доход) или "expense" (расход)

    def __str__(self):
        """строковое представление транзакции."""
        return f"{self.date.strftime('%Y-%m-%d')} | {self.type.upper()} | {self.category}: {self.amount} руб."

    def __eq__(self, other):
        """Сравнивает две транзакции по содержимому."""
        if not isinstance(other, Transaction):
            return False
        return (
            self.amount == other.amount
            and self.category == other.category
            and self.date == other.date
            and self.type == other.type
        )
    
    def __hash__(self):
        """
        Возвращает хэш транзакции для использования в множествах и словарях.
        """
        return hash((self.amount, self.category, self.date, self.type))
