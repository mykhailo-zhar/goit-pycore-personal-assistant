import re

from src.fields.field import Field


class Title(Field):
    """Клас для зберігання заголовку контакту.

    Аргументи:
          Field: Базовий клас для всіх полів.
    """

    TITLE_PATTERN = re.compile(r"(^[\w-]{1,100})$")

    def validate(self):
        """Перевіряє заголовок.

        Повертає:
            bool: True, якщо заголовок не довше 100 символів, інакше False.
        """
        return (
            re.match(self.TITLE_PATTERN, self.value) is not None
            and len(self.value.split()) <= 100
        )
