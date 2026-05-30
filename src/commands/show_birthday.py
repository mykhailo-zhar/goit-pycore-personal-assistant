from src.address_book import AddressBook
from src.utils.decorators.input_error import input_error

SHOW_BIRTHDAY_MESSAGES = {
    "INVALID_COMMAND": "Invalid command.",
    "NO_SUCH_USER": "No such user",
    "NO_BIRTHDAY_SET": "No birthday set for {name}",
    "BIRTHDAY_SHOWED": "Birthday for {name} is {birthday}",
}


@input_error
def show_birthday(book: AddressBook, arguments: list[str]) -> str:
    """Показує день народження контакту.

    Аргументи:
        book (AddressBook): Адресна книга.
        arguments (list[str]): Ім'я контакту.

    Повертає:
        str: Відповідь на команду.

    Винятки:
        ValueError: Якщо синтаксис команди невірний, контакт не знайдено
            або день народження не встановлено.
    """
    if len(arguments) != 1:
        raise ValueError(SHOW_BIRTHDAY_MESSAGES["INVALID_COMMAND"])
    name = arguments[0]
    record = book.find_record(name)
    if not record:
        raise ValueError(SHOW_BIRTHDAY_MESSAGES["NO_SUCH_USER"])
    if not record.birthday:
        raise ValueError(SHOW_BIRTHDAY_MESSAGES["NO_BIRTHDAY_SET"].format(name=name))
    return SHOW_BIRTHDAY_MESSAGES["BIRTHDAY_SHOWED"].format(
        name=name, birthday=record.birthday.value
    )
