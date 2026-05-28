import sys
from functools import wraps
from pathlib import Path

from src.record import Record
from src.utils.address_book_serializer import AddressBookSerializer

if __name__ == "__main__":
    sys.path.append(str(Path(__file__).resolve().parents[2]))


from src.address_book import AddressBook

COMMAND_MESSAGES = {
    "INVALID_COMMAND": "Invalid command.",
    "CONTACT_ADDED": "Contact added.",
    "CONTACT_UPDATED": "Contact updated.",
    "ADDRESS_ADDED": "Address added.",
    "BIRTHDAY_ADDED": "Birthday added. Replacing {old_birthday} with {new_birthday} for {name}",
    "NO_BIRTHDAY_SET": "No birthday set for {name}",
    "BIRTHDAY_SHOWED": "Birthday for {name} is {birthday}",
    "UPCOMING_BIRTHDAYS": "Upcoming birthdays:\n{birthdays}",
    "NO_SUCH_USER": "No such user",
    "PLEASE_CHANGE_USER": "Please change the user",
    "GOOD_BYE": "Good bye!",
    "NO_USERS": "There are no users",
    "HELLO": "How can I help you?",
    "PHONE_ALREADY_EXISTS": "Phone already exists",
    "NO_CONTACTS_BY_ADDRESS": "No contacts found by address",
    "CONTACTS_BY_ADDRESS": "Contacts by address:\n{contacts}",
}

SERIALIZER_PATH = "addressbook.pkl"


def input_error(func):
    """Декоратор для обробки помилок введення."""

    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except (ValueError, TypeError, IndexError, KeyError) as e:
            return str(e)

    return wrapper


def serializes(func, object, serializer=None):
    """
    Декоратор для збереження адресної книги після команди.

    Аргументи:
        func (Callable): Функція-обробник.
        object (Any): Об'єкт для серіалізації.
        serializer (AddressBookSerializer | None): Серіалізатор.

    Повертає:
        Callable: Обгорнута функція.
    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        if serializer:
            serializer.serialize(object)
        return result

    return wrapper


def parse_input(line: str) -> tuple[str, list[str]]:
    """
    Розбирає рядок введення на команду та аргументи.

    Аргументи:
        line (str): Рядок від користувача.

    Повертає:
        tuple[str, list[str]]: Команда та список аргументів.
    """
    if line.strip() == "":
        return "", []
    arguments = line.split()
    return arguments[0].lower(), arguments[1:]


@input_error
def hello(_: AddressBook, arguments: list[str] = []) -> str:
    """
    Команда привітання.

    Аргументи:
        _ (AddressBook): Адресна книга.
        arguments (list[str]): Аргументи команди.

    Повертає:
        str: Привітальне повідомлення.
    """
    if arguments:
        raise ValueError(COMMAND_MESSAGES["INVALID_COMMAND"])

    return COMMAND_MESSAGES["HELLO"]


@input_error
def add_contact(book: AddressBook, arguments: list[str]) -> str:
    """
    Додає контакт або телефон до існуючого.

    Аргументи:
        book (AddressBook): Адресна книга.
        arguments (list[str]): Ім'я та телефон.

    Повертає:
        str: Відповідь на команду.
    """
    if len(arguments) != 2:
        raise ValueError(COMMAND_MESSAGES["INVALID_COMMAND"])
    name, phone = arguments
    existing_record = book.find_record(name)

    if existing_record:
        for existing_phone in existing_record.phones:
            if existing_phone.value == phone:
                raise ValueError(COMMAND_MESSAGES["PHONE_ALREADY_EXISTS"])


        existing_record.add_phone(phone)
    else:
        record = Record(name)
        record.add_phone(phone)
        book.add_record(record)

    return COMMAND_MESSAGES["CONTACT_ADDED"]


@input_error
def update_contact(book: AddressBook, arguments: list[str]) -> str:
    """
    Оновлює телефони контакту.

    Аргументи:
        book (AddressBook): Адресна книга.
        arguments (list[str]): Ім'я та новий телефон.

    Повертає:
        str: Відповідь на команду.

    Примітки:
        Замінює всі телефони контакту одним вказаним номером.
    """
    if len(arguments) != 2:
        raise ValueError(COMMAND_MESSAGES["INVALID_COMMAND"])
    name, phone = arguments
    record = Record(name)
    record.add_phone(phone)

    if not book.remove_record(name):
        raise ValueError(COMMAND_MESSAGES["NO_SUCH_USER"])

    book.add_record(record)

    return COMMAND_MESSAGES["CONTACT_UPDATED"]


@input_error
def add_birthday(book: AddressBook, arguments: list[str]) -> str:
    """
    Додає день народження контакту.

    Аргументи:
        book (AddressBook): Адресна книга.
        arguments (list[str]): Ім'я та дата DD.MM.YYYY.

    Повертає:
        str: Відповідь на команду.
    """
    if len(arguments) != 2:
        raise ValueError(COMMAND_MESSAGES["INVALID_COMMAND"])
    name, birthday = arguments
    record = book.find_record(name)
    if not record:
        raise ValueError(COMMAND_MESSAGES["NO_SUCH_USER"])
    old_birthday = record.birthday.value if record.birthday else None
    record.add_birthday(birthday)
    return COMMAND_MESSAGES["BIRTHDAY_ADDED"].format(
        old_birthday=old_birthday,
        new_birthday=birthday,
        name=name,
    )


@input_error
def add_address(book: AddressBook, arguments: list[str]) -> str:
    """
    Додає адресу до існуючого контакту.

    Аргументи:
        book (AddressBook): Адресна книга.
        arguments (list[str]): Ім'я контакту та адреса.

    Повертає:
        str: Відповідь на команду.
    """
    if len(arguments) < 2:
        raise ValueError(COMMAND_MESSAGES["INVALID_COMMAND"])
    name = arguments[0]
    address = " ".join(arguments[1:])
    record = book.find_record(name)
    if not record:
        raise ValueError(COMMAND_MESSAGES["NO_SUCH_USER"])
    record.add_address(address)
    return COMMAND_MESSAGES["ADDRESS_ADDED"]


@input_error
def find_contacts_by_address(book: AddressBook, arguments: list[str]) -> str:
    """
    Шукає контакти за адресою.

    Аргументи:
        book (AddressBook): Адресна книга.
        arguments (list[str]): Адреса або частина адреси для пошуку.

    Повертає:
        str: Знайдені контакти або повідомлення, що контактів немає.
    """
    if len(arguments) < 1:
        raise ValueError(COMMAND_MESSAGES["INVALID_COMMAND"])
    search_address = " ".join(arguments).lower()
    found_contacts = []

    for record in book.data.values():
        if record.address:
            if search_address in record.address.value.lower():
                found_contacts.append(str(record))
    if not found_contacts:
        return COMMAND_MESSAGES["NO_CONTACTS_BY_ADDRESS"]
    return COMMAND_MESSAGES["CONTACTS_BY_ADDRESS"].format(
        contacts="\n".join(found_contacts)
    )


@input_error
def show_birthday(book: AddressBook, arguments: list[str]) -> str:
    """
    Показує день народження контакту.

    Аргументи:
        book (AddressBook): Адресна книга.
        arguments (list[str]): Ім'я контакту.

    Повертає:
        str: Відповідь на команду.
    """
    if len(arguments) != 1:
        raise ValueError(COMMAND_MESSAGES["INVALID_COMMAND"])
    name = arguments[0]
    record = book.find_record(name)
    if not record:
        raise ValueError(COMMAND_MESSAGES["NO_SUCH_USER"])
    if not record.birthday:
        raise ValueError(COMMAND_MESSAGES["NO_BIRTHDAY_SET"].format(name=name))
    return COMMAND_MESSAGES["BIRTHDAY_SHOWED"].format(
        name=name, birthday=record.birthday.value
    )


@input_error
def show_phone(book: AddressBook, arguments: list[str]) -> str:
    """
    Показує телефон(и) контакту.

    Аргументи:
        book (AddressBook): Адресна книга.
        arguments (list[str]): Ім'я контакту.

    Повертає:
        str: Номер(и) телефону.
    """
    if len(arguments) != 1:
        raise ValueError(COMMAND_MESSAGES["INVALID_COMMAND"])
    name = arguments[0]
    record = book.find_record(name)
    if not record:
        raise ValueError(COMMAND_MESSAGES["NO_SUCH_USER"])
    return "; ".join(phone.value for phone in record.phones)


@input_error
def birthdays(book: AddressBook, arguments: list[str] = []) -> str:
    """
    Показує найближчі дні народження.

    Аргументи:
        book (AddressBook): Адресна книга.
        arguments (list[str]): Аргументи команди.

    Повертає:
        str: Відповідь на команду.
    """
    if arguments:
        raise ValueError(COMMAND_MESSAGES["INVALID_COMMAND"])
    if not book.data:
        raise ValueError(COMMAND_MESSAGES["NO_USERS"])
    upcoming_birthdays = book.get_upcoming_birthdays()
    return COMMAND_MESSAGES["UPCOMING_BIRTHDAYS"].format(
        birthdays="\n".join(
            "{birthday} {name}".format(
                birthday=record.birthday.format(book.today),
                name=record.name,
            )
            for record in upcoming_birthdays
        )
    )


@input_error
def show_all(book: AddressBook, arguments: list[str] = []) -> str:
    """
    Показує всіх контактів.

    Аргументи:
        book (AddressBook): Адресна книга.
        arguments (list[str]): Аргументи команди.

    Повертає:
        str: Відповідь на команду.
    """
    if arguments:
        raise ValueError(COMMAND_MESSAGES["INVALID_COMMAND"])
    if not book.data:
        raise ValueError(COMMAND_MESSAGES["NO_USERS"])

    count_users = len(book.data)
    users_list = [str(record) for _, record in sorted(book.data.items())]
    users_text = "\n".join(users_list)

    return f"Stored users ({count_users}):\n{users_text}"


@input_error
def exit(_: AddressBook, arguments: list[str] = []) -> str:
    """
    Завершує роботу програми.

    Аргументи:
        _ (AddressBook): Адресна книга.
        arguments (list[str], optional): Аргументи команди.

    Повертає:
        str: Прощальне повідомлення.
    """
    if arguments:
        raise ValueError(COMMAND_MESSAGES["INVALID_COMMAND"])
    return COMMAND_MESSAGES["GOOD_BYE"]


def handle_command(
    book: AddressBook,
    command: str,
    arguments: list[str],
    serializer: AddressBookSerializer = None,
) -> str:
    """
    Виконує команду користувача.

    Аргументи:
        book (AddressBook): Адресна книга.
        command (str): Назва команди.
        arguments (list[str]): Аргументи команди.
        serializer (AddressBookSerializer | None): Серіалізатор для збереження.

    Повертає:
        str: Відповідь на команду.
    """
    commands = {
        "hello": hello,
        "add": serializes(add_contact, book, serializer),
        "update": serializes(update_contact, book, serializer),
        "phone": show_phone,
        "all": show_all,
        "add-birthday": serializes(add_birthday, book, serializer),
        "add-address": serializes(add_address, book, serializer),
        "find-address": find_contacts_by_address,
        "show-birthday": show_birthday,
        "birthdays": birthdays,
        "exit": exit,
        "close": exit,
    }

    if command not in commands:
        return COMMAND_MESSAGES["INVALID_COMMAND"]

    return commands[command](book, arguments)


def main() -> None:
    """Головна функція CLI-бота."""
    serializer: AddressBookSerializer = AddressBookSerializer(
        SERIALIZER_PATH, lambda message: print(message)
    )
    book: AddressBook = serializer.deserialize()
    while True:
        line = input()
        command, arguments = parse_input(line)
        response = handle_command(book, command, arguments, serializer)
        print(response)
        if command in ["exit", "close"]:
            break


if __name__ == "__main__":
    main()
