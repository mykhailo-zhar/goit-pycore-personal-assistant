from datetime import datetime

from src.fields.field import Field


class Birthday(Field):
    DATE_FORMAT = "%d.%m.%Y"
    """
    Зберігає день народження контакту.

    Аргументи:
        Field: Базовий клас для всіх полів.
    """

    def validate(self):
        """Перевіряє день народження."""

        try:
            datetime.strptime(self.value, self.DATE_FORMAT)
            return True
        except (ValueError, TypeError):
            return False

    def format(self, today=datetime.now()):
        """
        Форматує день народження як DD.MM.YYYY (День тижня).

        Аргументи:
            today (datetime): Поточна дата.

        Повертає:
            str: Відформатована дата у вигляді DD.MM.YYYY (День тижня).
        """
        birthdate = datetime.strptime(self.value, self.DATE_FORMAT)
        birthdate = birthdate.replace(year=today.year)
        return birthdate.strftime(f"{self.DATE_FORMAT} (%A)")
