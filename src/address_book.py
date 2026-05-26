from datetime import datetime

from src.record import Record
from src.utils.processed_record import ProcessedRecord


class AddressBook:
    def __init__(self):
        """Ініціалізує адресну книгу."""
        self.data = {}

    def add_record(self, record: Record):
        """
        Додає запис до адресної книги.

        Аргументи:
            record (Record): Запис для додавання.
        """
        self.data[record.name.value] = record

    def find_record(self, name: str) -> Record | None:
        """
        Шукає запис у адресній книзі.

        Аргументи:
            name (str): Ім'я контакту.

        Повертає:
            Record | None: Запис, якщо знайдено, інакше None.
        """
        return self.data.get(name)

    def remove_record(self, name: str) -> bool:
        """
        Видаляє запис з адресної книги.

        Аргументи:
            name (str): Ім'я контакту.

        Повертає:
            bool: True, якщо запис видалено, інакше False.
        """

        return self.data.pop(name, None) is not None

    @property
    def today(self) -> datetime:
        """
        Повертає поточну дату.

        Повертає:
            datetime: Поточна дата.
        """
        return self.__today

    def get_upcoming_birthdays(self) -> list[Record]:
        """
        Повертає найближчі дні народження з адресної книги.

        Повертає:
            list[Record]: Список записів, відсортований за датою привітання.
        """

        def __init__(self):
            self.__today = datetime.now()

        if not self.data:
            return []

        # Записи без дня народження не потрапляють у список
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
