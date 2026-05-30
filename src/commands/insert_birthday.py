from src.address_book import AddressBook
from src.utils.decorators.input_error import input_error

INSERT_BIRTHDAY_MESSAGES = {
    "INVALID_COMMAND": "Invalid command.",
    "BIRTHDAY_ADDED": "Birthday added. Replacing {old_birthday} with {new_birthday} for {name}",
    "NO_SUCH_USER": "No such user",
}


@input_error
def insert_birthday(book: AddressBook, arguments: list[str]) -> str:
    """Додає день народження контакту.

    Аргументи:
        book (AddressBook): Адресна книга.
        arguments (list[str]): Ім'я та дата DD.MM.YYYY.

    Повертає:
        str: Відповідь на команду.

    Винятки:
        ValueError: Якщо синтаксис команди невірний або контакт не знайдено.
    """
    if len(arguments) != 2:
        raise ValueError(INSERT_BIRTHDAY_MESSAGES["INVALID_COMMAND"])
    name, birthday = arguments
    record = book.find_record(name)
    if not record:
        raise ValueError(INSERT_BIRTHDAY_MESSAGES["NO_SUCH_USER"])
    old_birthday = record.birthday.value if record.birthday else None
    record.add_birthday(birthday)
    return INSERT_BIRTHDAY_MESSAGES["BIRTHDAY_ADDED"].format(
        old_birthday=old_birthday,
        new_birthday=birthday,
        name=name,
    )
