from ..fields.field import Field


class Address(Field):
    """Клас для зберігання фізичної адреси контакту.

    Аргументи:
          Field: Базовий клас для всіх полів.
    """

    def validate(self):
        """
        Перевіряє адресу.

        Повертає:
            bool: True, якщо адреса не пуста, інакше False.
        """
        return bool(self.value and self.value.strip())
