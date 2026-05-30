from src.address_book import AddressBook
from src.decorators.input_error import input_error
from src.record import ADDRESS_NOT_VALID_ERROR

INSERT_ADDRESS_MESSAGES = {
    "INVALID_SYNTAX": "Insert address command should have the following syntax: insert-address <name> <address>",
    "ADDRESS_ADDED": "Address added.",
    "ADDRESS_REPLACED": "Replacing {old_address} with {new_address} for {name}",
    "NO_SUCH_CONTACT": "No such contact.",
    "ADDRESS_NOT_VALID": ADDRESS_NOT_VALID_ERROR,
}


@input_error
def insert_address(book: AddressBook, arguments: list[str]) -> str:
    """
    Додає або оновлює адресу контакту.

    Аргументи:
        book (AddressBook): Адресна книга.
        arguments (list[str]): Ім'я та адреса.
    """
    if len(arguments) < 2:
        raise ValueError(INSERT_ADDRESS_MESSAGES["INVALID_SYNTAX"])

    name = arguments[0]
    address = " ".join(arguments[1:])

    record = book.find_record(name)
    if not record:
        raise ValueError(INSERT_ADDRESS_MESSAGES["NO_SUCH_CONTACT"])

    old_address = record.address.value if record.address else None

    try:
        record.address = address
    except ValueError as err:
        if str(err) == ADDRESS_NOT_VALID_ERROR:
            raise ValueError(INSERT_ADDRESS_MESSAGES["ADDRESS_NOT_VALID"])
        raise

    if old_address:
        return INSERT_ADDRESS_MESSAGES["ADDRESS_REPLACED"].format(
            old_address=old_address,
            new_address=address,
            name=name,
        )
    return INSERT_ADDRESS_MESSAGES["ADDRESS_ADDED"]
