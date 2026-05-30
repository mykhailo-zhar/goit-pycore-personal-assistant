from src.address_book import AddressBook
from src.utils.decorators.input_error import input_error

SHOW_PHONE_MESSAGES = {
    "INVALID_COMMAND": "Invalid command.",
    "NO_SUCH_USER": "No such user",
}


@input_error
def show_phone(book: AddressBook, arguments: list[str]) -> str:
    """Показує телефон(и) контакту.

    Аргументи:
        book (AddressBook): Адресна книга.
        arguments (list[str]): Ім'я контакту.

    Повертає:
        str: Номер(и) телефону.

    Винятки:
        ValueError: Якщо синтаксис команди невірний або контакт не знайдено.
    """
    if len(arguments) != 1:
        raise ValueError(SHOW_PHONE_MESSAGES["INVALID_COMMAND"])
    name = arguments[0]
    record = book.find_record(name)
    if not record:
        raise ValueError(SHOW_PHONE_MESSAGES["NO_SUCH_USER"])
    return "; ".join(phone.value for phone in record.phones)
