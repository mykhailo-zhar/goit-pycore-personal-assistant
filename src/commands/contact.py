from src.address_book import AddressBook
from src.decorators.input_error import input_error
from src.presenters.record import RecordPresenter

CONTACT_MESSAGES = {
    "INVALID_SYNTAX": "Contact command should have the following syntax: contact <name>",
    "NO_SUCH_CONTACT": "No such contact.",
}


@input_error
def contact(book: AddressBook, arguments: list[str]) -> str:
    """
    Показує інформацію про контакт за іменем.

    Аргументи:
        book (AddressBook): Адресна книга.
        arguments (list[str]): Ім'я контакту.
    """
    if len(arguments) != 1:
        raise ValueError(CONTACT_MESSAGES["INVALID_SYNTAX"])

    name = arguments[0]
    record = book.find_record(name)
    if record is None:
        raise ValueError(CONTACT_MESSAGES["NO_SUCH_CONTACT"])

    return str(RecordPresenter(record))
