import sys
from pathlib import Path

from src.commands import (
    add_note,
    add_tag,
    change_title,
    find_by_tag,
    insert_address,
    insert_email,
    insert_text,
    remove_contact,
    remove_tag,
    show_all,
    show_note,
    )
from src.record import Record
from src.utils.decorators.input_error import input_error
from src.utils.decorators.serializes import serializes
from src.utils.serializers.address_book import AddressBookSerializer
from src.utils.serializers.note_book import NoteBookSerializer

if __name__ == "__main__":
    sys.path.append(str(Path(__file__).parent[3].absolute()))

from src.address_book import AddressBook
from src.note_book import NoteBook
from messages import COMMAND_MESSAGES

SERIALIZER_PATH = "addressbook.pkl"
NOTE_SERIALIZER_PATH = "notebook.pkl"


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
    record = Record(name)
    if record := book.find_record(name):
        record.add_phone(phone)
    else:
        record = Record(name)
        record.add_phone(phone)
        book.add_record(record)
    return COMMAND_MESSAGES["CONTACT_ADDED"]


@input_error
def change_phone(book: AddressBook, arguments: list[str]) -> str:
    """
    Змінює телефон контакту.

    Аргументи:
        book (AddressBook): Адресна книга.
        arguments (list[str]): Ім'я, старий телефон та новий телефон.

    Повертає:
        str: Відповідь на команду.
    """
    if len(arguments) != 3:
        raise ValueError(COMMAND_MESSAGES["PHONE_CHANGE_SYNTAX"])

    name, old_phone, new_phone = arguments

    record = book.find_record(name)
    if record is None:
        raise KeyError(COMMAND_MESSAGES["NO_SUCH_USER"])

    record.edit_phone(old_phone, new_phone)

    return COMMAND_MESSAGES["PHONE_CHANGED"]


@input_error
def truncate_contact(book: AddressBook, arguments: list[str]) -> str:
    """
    Очищає всі телефони контакту і додає один новий.
    """

    if len(arguments) != 2:
        raise ValueError(COMMAND_MESSAGES["TRUNCATE_SYNTAX"])

    name, phone = arguments

    record = book.find_record(name)

    if record is None:
        raise KeyError(COMMAND_MESSAGES["NO_SUCH_USER"])
    old_phones = record.phones.copy()

    try:
        record.phones.clear()
        record.add_phone(phone)
    except ValueError:
        record.phones.extend(old_phones)
        raise

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
def birthdays(book: AddressBook, arguments: list[str]) -> str:
    """
    Показує найближчі дні народження.

    Аргументи:
        book (AddressBook): Адресна книга.
        arguments (list[str]): Аргументи команди.

    Повертає:
        str: Відповідь на команду.
    """
    if len(arguments) != 1:
        raise ValueError(COMMAND_MESSAGES["BIRTHDAYS_SYNTAX"])
    if not arguments[0].isdigit():
        raise ValueError(COMMAND_MESSAGES["BIRTHDAYS_DAYS"])

    days = int(arguments[0])

    processed_records = book.get_upcoming_birthdays(days)

    if not processed_records:
        return COMMAND_MESSAGES["BIRTHDAYS_NO_UPCOMMING"]

    lines = [
        f"{pr.record.name.value}: {pr.congratulation_date.strftime(COMMAND_MESSAGES['BIRTHDAYS_FORMAT'])}"
        for pr in processed_records
        ]
    return "\n".join(lines)


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
        note_book: NoteBook,
        command: str,
        arguments: list[str],
        serializer: AddressBookSerializer = None,
        note_serializer: NoteBookSerializer = None,
        ) -> str:
    """
    Виконує команду користувача.

    Аргументи:
        book (AddressBook): Адресна книга.
        note_book (NoteBook): Книга нотаток.
        command (str): Назва команди.
        arguments (list[str]): Аргументи команди.
        serializer (AddressBookSerializer | None): Серіалізатор адресної книги.
        note_serializer (NoteBookSerializer | None): Серіалізатор книги нотаток.

    Повертає:
        str: Відповідь на команду.
    """
    commands = {
        "hello": hello,
        "add": serializes(add_contact, book, serializer),
        "truncate": serializes(truncate_contact, book, serializer),
        "change-phone": serializes(change_phone, book, serializer),
        "remove": serializes(remove_contact, book, serializer),
        "insert-address": serializes(insert_address, book, serializer),
        "phone": show_phone,
        "all": show_all,
        "add-birthday": serializes(add_birthday, book, serializer),
        "insert-email": serializes(insert_email, book, serializer),
        "show-birthday": show_birthday,
        "birthdays": birthdays,
        "add-note": serializes(
            lambda _book, args: add_note(note_book, args), note_book,
            note_serializer
            ),
        "insert-text": serializes(
            lambda _book, args: insert_text(note_book, args),
            note_book,
            note_serializer,
            ),
        "change-title": serializes(
            lambda _book, args: change_title(note_book, args),
            note_book,
            note_serializer,
            ),
        "note": lambda _book, args: show_note(note_book, args),
        "add-tag": serializes(
            lambda _book, args: add_tag(note_book, args), note_book,
            note_serializer
            ),
        "remove-tag": serializes(
            lambda _book, args: remove_tag(note_book, args),
            note_book,
            note_serializer,
            ),
        "tag": lambda _book, args: find_by_tag(note_book, args),
        "exit": exit,
        "close": exit,
        }

    if command not in commands:
        return COMMAND_MESSAGES["INVALID_COMMAND"]

    return commands[command](book, arguments)


def _print_warning(message: str) -> None:
    print(message)


def main() -> None:
    """Головна функція CLI-бота."""
    serializer: AddressBookSerializer = AddressBookSerializer(
        SERIALIZER_PATH, _print_warning
        )
    note_serializer: NoteBookSerializer = NoteBookSerializer(
        NOTE_SERIALIZER_PATH, _print_warning
        )
    book: AddressBook = serializer.deserialize()
    note_book: NoteBook = note_serializer.deserialize()
    print(
        f"Bot is started. Type 'hello' to greet, 'help' for commands list, 'exit' or 'close' to quit.")
    try:
        while True:
            line = input().strip()

            if not line:
                continue

            command, arguments = parse_input(line)
            response = handle_command(
                book, note_book, command, arguments, serializer,
                note_serializer
                )
            print(response)
            if command in ["exit", "close"]:
                break
    except (KeyboardInterrupt, EOFError):
        print(f"\n{COMMAND_MESSAGES['GOOD_BYE']}")


if __name__ == "__main__":
    main()
