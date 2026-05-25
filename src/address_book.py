from datetime import datetime

from src.record import Record
from src.utils.processed_record import ProcessedRecord


class AddressBook:
    def __init__(self):
        """
        Initialize the address book.
        """
        self.data = {}

    def add_record(self, record: Record):
        """
        Add a record to the address book.

        Args:
            record (Record): The record to add.
        """
        self.data[record.name.value] = record

    def find_record(self, name: str) -> Record | None:
        """
        Find a record in the address book.

        Args:
            name (str): The name of the record to find.

        Returns:
            Record | None: The record if found, None otherwise.
        """
        return self.data.get(name)

    def remove_record(self, name: str) -> bool:
        """
        Remove a record from the address book.

        Args:
            name (str): The name of the record to remove.

        Returns:
            bool: True if the record was removed, False otherwise.
        """

        return self.data.pop(name, None) is not None

    @property
    def today(self) -> datetime:
        """
        Get the today's date.

        Returns:
            datetime: The today's date.
        """
        return self.__today

    def get_upcoming_birthdays(self) -> list[Record]:
        """
        Get the upcoming birthdays from the address book.

        Returns:
            list[Record]: List of upcoming birthdays sorted by congratulation date.
        """

        if not self.data:
            return []

        self.__today = datetime.now()

        # Records without birthday may cause a crash
        processed_records = [
            ProcessedRecord(record, self.__today)
            for record in self.data.values()
            if record.birthday
        ]

        upcoming_birthdays = filter(
            ProcessedRecord.is_congratulation_date_in_next_7_days(self.__today),
            processed_records,
        )

        sorted_upcoming_birthdays = sorted(
            upcoming_birthdays, key=lambda record: record.congratulation_date
        )

        return list(map(lambda record: record.record, sorted_upcoming_birthdays))
