from collections.abc import Callable
from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Self

from src.fields.birthday import Birthday
from src.record import Record


@dataclass(init=False)
class ProcessedRecord:
    """
    Processed record.

    Args:
        record (Record): The record to process.
        today (datetime): The today's date.
    """

    record: Record
    congratulation_date: datetime

    def __init__(self, record: Record, today: datetime):
        """
        Initialize the processed record.

        Args:
            record (Record): The record to process.
            today (datetime): The today's date.
        """
        self.__record = record
        self.__today = today
        self.__congratulation_date = self.__calculate_congratulation_date()

    @property
    def record(self) -> Record:
        """
        Get the record.

        Returns:
            Record: The record.
        """
        return self.__record

    @record.setter
    def record(self, record: Record):
        """
        Set the record.

        Args:
            record: The record to set.

        Notes:
            This method will recalculate the congratulation date.
        """
        self.__record = record
        self.__congratulation_date = self.__calculate_congratulation_date()

    @property
    def congratulation_date(self) -> datetime:
        """
        Get the congratulation date.

        Returns:
            datetime: The congratulation date.
        """
        return self.__congratulation_date

    @staticmethod
    def is_congratulation_date_in_next_7_days(
        today: datetime,
    ) -> Callable[[Self], bool]:
        """
        Check if the congratulation date is in the next 7 days.

        Args:
            today: The today's date.

        Returns:
            Callable[[ProcessedRecord], bool]: Curry function
        """
        return lambda record: (
            record.congratulation_date >= today
            and record.congratulation_date < (today + timedelta(days=7))
        )

    def __calculate_congratulation_date(self) -> datetime:
        """
        Transform the birthday to the congratulation date.

        Args:
            birthday: The birthday of the user.

        Returns:
            The congratulation date.
        """
        birthday_date = datetime.strptime(
            self.record.birthday.value, Birthday.DATE_FORMAT
        )
        congratulation_date = birthday_date.replace(year=self.__today.year)

        weekday = congratulation_date.weekday()

        # Move the congratulation date to the next Monday if it's on a weekend
        if weekday in [5, 6]:
            congratulation_date = congratulation_date + timedelta(days=7 - weekday)

        return congratulation_date
