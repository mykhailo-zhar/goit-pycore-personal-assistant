from src.address_book import AddressBook
from src.utils.decorators.input_error import input_error

HELLO_MESSAGES = {
    "INVALID_COMMAND": "Invalid command.",
    "HELLO": "How can I help you?",
}


@input_error
def hello(_: AddressBook, arguments: list[str] = []) -> str:
    """Команда привітання.

    Аргументи:
        _ (AddressBook): Адресна книга.
        arguments (list[str]): Аргументи команди.

    Повертає:
        str: Привітальне повідомлення.

    Винятки:
        ValueError: Якщо передано зайві аргументи.
    """
    if arguments:
        raise ValueError(HELLO_MESSAGES["INVALID_COMMAND"])

    return HELLO_MESSAGES["HELLO"]
