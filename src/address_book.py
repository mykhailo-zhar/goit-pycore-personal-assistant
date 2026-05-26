from datetime import datetime, timedelta

from src.record import Record


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

    def get_upcoming_birthdays(self) -> list[dict]:
        """Function to get upcoming birthdays from records"""

        today_date = datetime.today()
        upcoming_birthdays = []

        for record in self.data.values():
            if not record.birthday:
                continue

            # Отримуємо дату народження з запису
            birthday_date_str = record.birthday.value
            # Припускаємо, що формат дати день.місяць.рік
            birthday_date = datetime.strptime(birthday_date_str, "%d.%m.%Y")

            # Встановлюємо поточний рік для дня народження
            birthday_this_year = birthday_date.replace(year=today_date.year)

            # Якщо день народження вже минув у цьому році, беремо наступний рік
            if birthday_this_year.date() < today_date.date():
                birthday_this_year = birthday_this_year.replace(
                    year=today_date.year + 1
                )

            days_to_birthday = (birthday_this_year.date() - today_date.date()).days

            # Перевіряємо, чи день народження у наступні 7 днів
            if 0 <= days_to_birthday <= 7:
                congratulation_date = birthday_this_year
                weekday = birthday_this_year.weekday()

                # Якщо день народження припадає на суботу (5) або неділю (6),
                # переносимо привітання на понеділок
                if weekday == 5:  # Субота
                    congratulation_date += timedelta(days=2)
                elif weekday == 6:  # Неділя
                    congratulation_date += timedelta(days=1)

                upcoming_birthdays.append(
                    {
                        "name": record.name.value,
                        "birthday": birthday_date.strftime("%d.%m.%Y"),
                        "congratulation_date": congratulation_date.strftime("%d.%m.%Y"),
                        "congratulation_weekday": congratulation_date.strftime("%A"),
                    }
                )

        return upcoming_birthdays
