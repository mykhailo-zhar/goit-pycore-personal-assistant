import re

from ..fields.field import Field


class Name(Field):
    """
    Зберігає ім'я контакту. Обов'язкове поле.

    Аргументи:
        Field: Базовий клас для всіх полів.
    """

    NAME_PATTERN = re.compile(r"^\w+$")

    def validate(self):
        """
        Перевіряє ім'я.

        Повертає:
            bool: True, якщо ім'я валідне, інакше False.
        """
        return (
            isinstance(self.value, str)
            and self.value != ""
            and re.match(self.NAME_PATTERN, self.value) is not None
        )
