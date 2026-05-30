from src.address_book import AddressBook
from src.utils.decorators.input_error import input_error

ADD_ADDRESS_MESSAGES = {
    "INVALID_COMMAND": "Invalid command.",
    "ADDRESS_ADDED": "Address added.",
    "NO_SUCH_USER": "No such user",
}


@input_error
def add_address(book: AddressBook, arguments: list[str]) -> str:
    """Додає адресу до існуючого контакту.

    Аргументи:
        book (AddressBook): Адресна книга.
        arguments (list[str]): Ім'я контакту та адреса.

    Повертає:
        str: Відповідь на команду.

    Винятки:
        ValueError: Якщо синтаксис команди невірний або контакт не знайдено.
    """
    if len(arguments) < 2:
        raise ValueError(ADD_ADDRESS_MESSAGES["INVALID_COMMAND"])
    name = arguments[0]
    address = " ".join(arguments[1:])
    record = book.find_record(name)
    if not record:
        raise ValueError(ADD_ADDRESS_MESSAGES["NO_SUCH_USER"])
    record.add_address(address)
    return ADD_ADDRESS_MESSAGES["ADDRESS_ADDED"]
