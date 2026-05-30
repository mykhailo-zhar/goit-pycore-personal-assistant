import sys
from pathlib import Path

from src.commands import (
    add_address,
    add_birthday,
    add_contact,
    add_note,
    add_tag,
    birthdays,
    change_phone,
    change_title,
    contact,
    contact_address,
    contact_email,
    exit_command,
    find_by_tag,
    find_contacts_by_address,
    hello,
    help_command,
    insert_address,
    insert_email,
    insert_text,
    remove_contact,
    remove_note,
    remove_tag,
    show_all,
    show_birthday,
    show_note,
    show_phone,
    truncate_contact,
)
from src.utils.decorators.serializes import serializes
from src.utils.serializers.address_book import AddressBookSerializer
from src.utils.serializers.note_book import NoteBookSerializer

if __name__ == "__main__":
    sys.path.append(str(Path(__file__).resolve().parents[2]))

from src.address_book import AddressBook
from src.note_book import NoteBook

COMMAND_MESSAGES = {
    "INVALID_COMMAND": "Invalid command.",
    "GOOD_BYE": "Good bye!",
}

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
        "contact": contact,
        "contact-address": contact_address,
        "contact-email": contact_email,
        "insert-birthday": serializes(add_birthday, book, serializer),
        "add-address": serializes(add_address, book, serializer),
        "find-address": find_contacts_by_address,
        "insert-email": serializes(insert_email, book, serializer),
        "show-birthday": show_birthday,
        "birthdays": birthdays,
        "add-note": serializes(
            lambda _book, args: add_note(note_book, args), note_book, note_serializer
        ),
        "remove-note": serializes(
            lambda _book, args: remove_note(note_book, args), note_book, note_serializer
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
            lambda _book, args: add_tag(note_book, args), note_book, note_serializer
        ),
        "remove-tag": serializes(
            lambda _book, args: remove_tag(note_book, args),
            note_book,
            note_serializer,
        ),
        "tag": lambda _book, args: find_by_tag(note_book, args),
        "exit": exit_command,
        "close": exit_command,
        "help": help_command,
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
        "Bot is started. Type 'hello' to greet, 'help' for commands list, 'exit' or 'close' to quit."
    )
    try:
        while True:
            line = input().strip()

            if not line:
                continue

            command, arguments = parse_input(line)
            response = handle_command(
                book, note_book, command, arguments, serializer, note_serializer
            )
            print(response)
            if command in ["exit", "close"]:
                break
    except (KeyboardInterrupt, EOFError):
        print(f"\n{COMMAND_MESSAGES['GOOD_BYE']}")


if __name__ == "__main__":
    main()
