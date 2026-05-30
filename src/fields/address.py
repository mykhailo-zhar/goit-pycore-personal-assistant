from src.fields.field import Field


class Address(Field):
    """
    Представляє адресу контакту.

    Адреса є текстовим полем і повинна бути непорожнім рядком.
    """

    def validate(self) -> bool:
        """
        Перевіряє валідність адреси.

        Повертає:
            bool: True, якщо адреса є непорожнім рядком.
        """
        return isinstance(self.value, str) and bool(self.value.strip())
