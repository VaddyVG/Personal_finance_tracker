from datetime import datetime
from prompt_toolkit.validation import Validator, ValidationError
from prompt_toolkit.completion import WordCompleter


class AmountValidator(Validator):
    '''Валидатор для чисел'''
    def validate(self, document):
        try:
            float(document.text)
        except ValueError:
            raise ValidationError(message="Сумма должна быть числом (например: 100 или 50.5)")


class DateValidator(Validator):
    def validate(self, document):
        try:
            datetime.strptime(document.text, '%Y-%m-%d')
        except ValueError:
            raise ValidationError(message="Неверный формат даты. Используйте ГГГГ-ММ-ДД (например: 2023-12-31)")


type_completer = WordCompleter(["income", "expense"], ignore_case=True)
