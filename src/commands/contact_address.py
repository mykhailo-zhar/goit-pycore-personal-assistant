from src.address_book import AddressBook
from src.utils.decorators.input_error import input_error

CONTACT_ADDRESS_MESSAGES = {
    "INVALID_SYNTAX": (
        "Contact address command should have the following syntax: "
        "contact-address <address>"
    ),
    "NO_SUCH_CONTACT": "No such contact.",
}


@input_error
def contact_address(book: AddressBook, arguments: list[str]) -> str:
    """
    Показує контакти за схожістю адреси.

    Аргументи:
        book (AddressBook): Адресна книга.
        arguments (list[str]): Адреса або частина адреси для пошуку.
    """
    if len(arguments) < 1:
        raise ValueError(CONTACT_ADDRESS_MESSAGES["INVALID_SYNTAX"])

    search_address = " ".join(arguments).lower()
    found_contacts = [
        str(record)
        for record in book.data.values()
        if record.address and search_address in record.address.value.lower()
    ]

    if not found_contacts:
        raise ValueError(CONTACT_ADDRESS_MESSAGES["NO_SUCH_CONTACT"])

    return "\n".join(found_contacts)
