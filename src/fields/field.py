class Field:
    """Базовий клас для всіх полів запису."""

    def __init__(self, value):
        """
        Ініціалізує поле значенням.

        Аргументи:
            value: Значення для збереження.
        """
        self.value = value

    def __str__(self):
        """Повертає рядкове подання поля."""
        return str(self.value)

    def validate(self):
        """
        Перевіряє коректність значення.

        Повертає:
            bool: True, якщо значення валідне, інакше False.
        """
        return True
