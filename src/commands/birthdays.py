from src.address_book import AddressBook
from src.decorators.input_error import input_error

BIRTHDAYS_MESSAGES = {
    "BIRTHDAYS_SYNTAX": "Syntax: birthdays <days>",
    "BIRTHDAYS_DAYS": "Days must be a non-negative integer.",
    "BIRTHDAYS_NO_UPCOMMING": "No upcoming birthdays.",
    "BIRTHDAYS_FORMAT": "%d.%m.%Y",
}


@input_error
def birthdays(book: AddressBook, arguments: list[str]) -> str:
    """Показує найближчі дні народження.

    Аргументи:
        book (AddressBook): Адресна книга.
        arguments (list[str]): Кількість днів для пошуку найближчих днів народження.

    Повертає:
        str: Відповідь на команду.

    Винятки:
        ValueError: Якщо синтаксис команди невірний або кількість днів невалідна.
    """
    if len(arguments) != 1:
        raise ValueError(BIRTHDAYS_MESSAGES["BIRTHDAYS_SYNTAX"])
    if not arguments[0].isdigit():
        raise ValueError(BIRTHDAYS_MESSAGES["BIRTHDAYS_DAYS"])

    days = int(arguments[0])

    processed_records = book.get_upcoming_birthdays(days)

    if not processed_records:
        return BIRTHDAYS_MESSAGES["BIRTHDAYS_NO_UPCOMMING"]

    lines = [
        f"{pr.record.name.value}: {pr.congratulation_date.strftime(BIRTHDAYS_MESSAGES['BIRTHDAYS_FORMAT'])}"
        for pr in processed_records
    ]
    return "\n".join(lines)
