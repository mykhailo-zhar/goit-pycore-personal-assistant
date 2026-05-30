from src.address_book import AddressBook
from src.record import Record
from src.utils.decorators.input_error import input_error

ADD_CONTACT_MESSAGES = {
    "INVALID_COMMAND": "Invalid command.",
    "CONTACT_ADDED": "Contact added.",
    "PHONE_ALREADY_EXISTS": "Phone already exists",
}


@input_error
def add_contact(book: AddressBook, arguments: list[str]) -> str:
    """Додає новий контакт або телефон до існуючого контакту.

    Аргументи:
        book (AddressBook): Адресна книга.
        arguments (list[str]): Ім'я контакту та номер телефону.

    Повертає:
        str: Відповідь на команду.

    Винятки:
        ValueError: Якщо синтаксис команди невірний або телефон уже існує.
    """
    if len(arguments) != 2:
        raise ValueError(ADD_CONTACT_MESSAGES["INVALID_COMMAND"])

    name, phone = arguments
    existing_record = book.find_record(name)

    if existing_record and existing_record.find_phone(phone):
        raise ValueError(ADD_CONTACT_MESSAGES["PHONE_ALREADY_EXISTS"])

    if existing_record:
        existing_record.add_phone(phone)
    else:
        record = Record(name)
        record.add_phone(phone)
        book.add_record(record)

    return ADD_CONTACT_MESSAGES["CONTACT_ADDED"]
