from src.address_book import AddressBook
from src.utils.decorators.input_error import input_error
from src.messages import INSERT_ADDRESS_MESSAGES, RECORD_MESSAGES


@input_error
def insert_address(book: AddressBook, arguments: list[str]) -> str:
    """
    Додає або оновлює адресу контакту.

    Аргументи:
        book (AddressBook): Адресна книга.
        arguments (list[str]): Ім'я та адреса.
    """
    if len(arguments) != 2:
        raise ValueError(INSERT_ADDRESS_MESSAGES["INVALID_SYNTAX"])

    name, address = arguments
    record = book.find_record(name)
    if not record:
        raise ValueError(INSERT_ADDRESS_MESSAGES["NO_SUCH_CONTACT"])

    old_address = record.address.value if record.address else None

    try:
        record.address = address
    except ValueError as err:
        if str(err) == RECORD_MESSAGES["ADDRESS_NOT_VALID_ERROR"]:
            raise ValueError(INSERT_ADDRESS_MESSAGES["ADDRESS_NOT_VALID"])
        raise

    if old_address:
        return INSERT_ADDRESS_MESSAGES["ADDRESS_REPLACED"].format(
            old_address=old_address,
            new_address=address,
            name=name,
            )
    return INSERT_ADDRESS_MESSAGES["ADDRESS_ADDED"]
