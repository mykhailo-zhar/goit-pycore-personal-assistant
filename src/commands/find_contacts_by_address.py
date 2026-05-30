from src.address_book import AddressBook
from src.decorators.input_error import input_error

FIND_CONTACTS_BY_ADDRESS_MESSAGES = {
    "INVALID_COMMAND": "Invalid command.",
    "NO_CONTACTS_BY_ADDRESS": "No contacts found by address",
    "CONTACTS_BY_ADDRESS": "Contacts by address:\n{contacts}",
}


@input_error
def find_contacts_by_address(book: AddressBook, arguments: list[str]) -> str:
    """Шукає контакти за адресою.

    Аргументи:
        book (AddressBook): Адресна книга.
        arguments (list[str]): Адреса або частина адреси для пошуку.

    Повертає:
        str: Знайдені контакти або повідомлення, що контактів немає.

    Винятки:
        ValueError: Якщо адресу для пошуку не передано.
    """
    if len(arguments) < 1:
        raise ValueError(FIND_CONTACTS_BY_ADDRESS_MESSAGES["INVALID_COMMAND"])
    search_address = " ".join(arguments).lower()
    found_contacts = [
        str(record)
        for record in book.data.values()
        if record.address and search_address in record.address.value.lower()
    ]

    if not found_contacts:
        return FIND_CONTACTS_BY_ADDRESS_MESSAGES["NO_CONTACTS_BY_ADDRESS"]

    return FIND_CONTACTS_BY_ADDRESS_MESSAGES["CONTACTS_BY_ADDRESS"].format(
        contacts="\n".join(found_contacts)
    )
