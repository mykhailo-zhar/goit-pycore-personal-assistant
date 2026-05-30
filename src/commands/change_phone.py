from src.address_book import AddressBook
from src.utils.decorators.input_error import input_error

CHANGE_PHONE_MESSAGES = {
    "NO_SUCH_USER": "No such user",
    "PHONE_CHANGED": "Phone was changed",
    "PHONE_CHANGE_SYNTAX": "Syntax: change-phone <name> <old phone> <new phone>",
}


@input_error
def change_phone(book: AddressBook, arguments: list[str]) -> str:
    """Змінює телефон контакту.

    Аргументи:
        book (AddressBook): Адресна книга.
        arguments (list[str]): Ім'я, старий телефон та новий телефон.

    Повертає:
        str: Відповідь на команду.

    Винятки:
        ValueError: Якщо синтаксис команди невірний.
        KeyError: Якщо контакт не знайдено.
    """
    if len(arguments) != 3:
        raise ValueError(CHANGE_PHONE_MESSAGES["PHONE_CHANGE_SYNTAX"])

    name, old_phone, new_phone = arguments

    record = book.find_record(name)
    if record is None:
        raise KeyError(CHANGE_PHONE_MESSAGES["NO_SUCH_USER"])

    record.edit_phone(old_phone, new_phone)

    return CHANGE_PHONE_MESSAGES["PHONE_CHANGED"]
