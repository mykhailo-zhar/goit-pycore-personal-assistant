from src.address_book import AddressBook
from src.utils.decorators.input_error import input_error

SHOW_ALL_MESSAGES = {
    "INVALID_SYNTAX": "Invalid command.",
    "NO_USERS": "There are no users.",
}


@input_error
def show_all(book: AddressBook, arguments: list[str] = []) -> str:
    """
    Показує всі контакти.

    Аргументи:
        book (AddressBook): Адресна книга.
        arguments (list[str]): Аргументи команди.

    Повертає:
        str: Відповідь на команду.
    """
    if arguments:
        raise ValueError(SHOW_ALL_MESSAGES["INVALID_SYNTAX"])
    if not book.data:
        raise ValueError(SHOW_ALL_MESSAGES["NO_USERS"])

    count_users = len(book.data)
    users_list = [str(record) for _, record in sorted(book.data.items())]
    return f"Stored users ({count_users}):\n{'\n'.join(users_list)}"
