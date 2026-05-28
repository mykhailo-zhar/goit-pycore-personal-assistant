import re

from ..fields.field import Field


class Email(Field):
    """Клас для Email з валідацією формату.

    Аргументи:
          Field: Базовий клас для всіх полів.
    """

    def validate(self):
        """Перевіряє email.

        Повертає:
            bool: True, якщо email валідний, інакше False.
        """
        return (
            re.match(r"^[a-z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2,}$", self.value) is not None
        )
