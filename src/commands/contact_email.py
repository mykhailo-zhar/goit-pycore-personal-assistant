from src.address_book import AddressBook
from src.decorators.input_error import input_error

CONTACT_EMAIL_MESSAGES = {
    "INVALID_SYNTAX": (
        "Contact email command should have the following syntax: contact-email <email>"
    ),
    "NO_SUCH_CONTACT": "No such contact.",
}


@input_error
def contact_email(book: AddressBook, arguments: list[str]) -> str:
    """
    Показує інформацію про контакт за повним email.

    Аргументи:
        book (AddressBook): Адресна книга.
        arguments (list[str]): Email контакту.
    """
    if len(arguments) != 1:
        raise ValueError(CONTACT_EMAIL_MESSAGES["INVALID_SYNTAX"])

    email = arguments[0]
    for record in book.data.values():
        if record.email and record.email.value == email:
            return str(record)

    raise ValueError(CONTACT_EMAIL_MESSAGES["NO_SUCH_CONTACT"])
