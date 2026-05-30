from src.address_book import AddressBook
from src.decorators.input_error import input_error

TRUNCATE_CONTACT_MESSAGES = {
    "CONTACT_UPDATED": "Contact updated.",
    "NO_SUCH_USER": "No such user",
    "TRUNCATE_SYNTAX": "Syntax: truncate <name> <new_phone>",
}


@input_error
def truncate_contact(book: AddressBook, arguments: list[str]) -> str:
    """Очищає всі телефони контакту і додає один новий.

    Аргументи:
        book (AddressBook): Адресна книга.
        arguments (list[str]): Ім'я контакту та новий номер телефону.

    Повертає:
        str: Відповідь на команду.

    Винятки:
        ValueError: Якщо синтаксис команди невірний або новий телефон невалідний.
        KeyError: Якщо контакт не знайдено.
    """
    if len(arguments) != 2:
        raise ValueError(TRUNCATE_CONTACT_MESSAGES["TRUNCATE_SYNTAX"])

    name, phone = arguments

    record = book.find_record(name)

    if record is None:
        raise KeyError(TRUNCATE_CONTACT_MESSAGES["NO_SUCH_USER"])
    old_phones = record.phones.copy()

    try:
        record.phones.clear()
        record.add_phone(phone)
    except ValueError:
        record.phones.extend(old_phones)
        raise

    return TRUNCATE_CONTACT_MESSAGES["CONTACT_UPDATED"]
