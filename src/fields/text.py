from ..fields.field import Field


class Text(Field):
    """Клас для зберігання тексту.

    Аргументи:
        Field: Базовий клас для всіх полів.
    """

    def validate(self):
        """Перевіряє текст.

        Повертає:
            bool: True, якщо текст валідний, інакше False.
        """
        return isinstance(self.value, str) and self.value.strip()
