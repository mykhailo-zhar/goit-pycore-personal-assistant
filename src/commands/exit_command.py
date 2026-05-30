from src.address_book import AddressBook
from src.decorators.input_error import input_error

EXIT_COMMAND_MESSAGES = {
    "INVALID_COMMAND": "Invalid command.",
    "GOOD_BYE": "Good bye!",
}


@input_error
def exit_command(_: AddressBook, arguments: list[str] = []) -> str:
    """Завершує роботу програми.

    Аргументи:
        _ (AddressBook): Адресна книга.
        arguments (list[str], optional): Аргументи команди.

    Повертає:
        str: Прощальне повідомлення.

    Винятки:
        ValueError: Якщо передано зайві аргументи.
    """
    if arguments:
        raise ValueError(EXIT_COMMAND_MESSAGES["INVALID_COMMAND"])
    return EXIT_COMMAND_MESSAGES["GOOD_BYE"]
