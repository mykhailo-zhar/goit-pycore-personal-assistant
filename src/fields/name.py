import re

from ..fields.field import Field


class Name(Field):
    """
    Зберігає ім'я контакту. Обов'язкове поле.

    Аргументи:
        Field: Базовий клас для всіх полів.
    """

    def validate(self):
        """
        Перевіряє ім'я.

        Повертає:
            bool: True, якщо ім'я валідне, інакше False.
        """
        return (
            isinstance(self.value, str)
            and self.value != ""
            and re.match(r"^\w+$", self.value) is not None
        )
