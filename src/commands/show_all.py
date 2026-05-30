from src.address_book import AddressBook
from src.decorators.input_error import input_error
from src.presenters.record import RecordPresenter

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
    users_list = [record for record in sorted(book.data.values())]
    return f"Stored contacts ({count_users}):\n{RecordPresenter(users_list)}"
