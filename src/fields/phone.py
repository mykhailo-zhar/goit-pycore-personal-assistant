import re

from ..fields.field import Field


class Phone(Field):
    """
    Зберігає номер телефону контакту.

    Аргументи:
        Field: Базовий клас для всіх полів.
    """

    def validate(self):
        """
        Перевіряє номер телефону.

        Повертає:
            bool: True, якщо номер валідний, інакше False.
        """
        return re.match(r"^\d{10}$", self.value) is not None
