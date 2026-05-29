from collections.abc import Callable
from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Self

from src.fields.birthday import Birthday
from src.record import Record


@dataclass(init=False)
class ProcessedRecord:
    """
    Оброблений запис з датою привітання.

    Аргументи:
        record (Record): Запис контакту.
        today (datetime): Поточна дата.
    """

    record: Record
    congratulation_date: datetime

    def __init__(self, record: Record, today: datetime):
        """
        Ініціалізує оброблений запис.

        Аргументи:
            record (Record): Запис контакту.
            today (datetime): Поточна дата.
        """
        self.__record = record
        self.__today = today
        self.__congratulation_date = self.__calculate_congratulation_date()

    @property
    def record(self) -> Record:
        """
        Повертає запис.

        Повертає:
            Record: Запис контакту.
        """
        return self.__record

    @record.setter
    def record(self, record: Record):
        """
        Встановлює запис.

        Аргументи:
            record: Запис для встановлення.

        Примітки:
            Перераховує дату привітання.
        """
        self.__record = record
        self.__congratulation_date = self.__calculate_congratulation_date()

    @property
    def congratulation_date(self) -> datetime:
        """
        Повертає дату привітання.

        Повертає:
            datetime: Дата привітання.
        """
        return self.__congratulation_date

    @staticmethod
    def is_congratulation_date_in_next_n_days(
        today: datetime, days: int
    ) -> Callable[[Self], bool]:
        """Перевіряє, чи дата привітання потрапляє в наступні n днів."""

        return lambda record: (
            today <= record.congratulation_date < (today + timedelta(days=days))
        )

    def __calculate_congratulation_date(self) -> datetime:
        """
        Обчислює дату привітання з дня народження.

        Повертає:
            datetime: Дата привітання (з урахуванням вихідних).
        """
        birthday_date = datetime.strptime(
            self.record.birthday.value, Birthday.DATE_FORMAT
        )
        congratulation_date = birthday_date.replace(year=self.__today.year)

        weekday = congratulation_date.weekday()

        # Перенос дати привітання на понеділок, якщо випадає на вихідні
        if weekday in [5, 6]:
            congratulation_date = congratulation_date + timedelta(days=7 - weekday)

        return congratulation_date
