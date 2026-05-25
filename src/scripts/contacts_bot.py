import sys
from functools import wraps
from pathlib import Path

from src.record import Record
from src.utils.address_book_serializer import AddressBookSerializer

if __name__ == "__main__":
    sys.path.append(str(Path(__file__).parent[3].absolute()))


from src.address_book import AddressBook

COMMAND_MESSAGES = {
    "INVALID_COMMAND": "Invalid command.",
    "CONTACT_ADDED": "Contact added.",
    "CONTACT_UPDATED": "Contact updated.",
    "BIRTHDAY_ADDED": "Birthday added. Replacing {old_birthday} with {new_birthday} for {name}",
    "NO_BIRTHDAY_SET": "No birthday set for {name}",
    "BIRTHDAY_SHOWED": "Birthday for {name} is {birthday}",
    "UPCOMING_BIRTHDAYS": "Upcoming birthdays:\n{birthdays}",
    "NO_SUCH_USER": "No such user",
    "PLEASE_CHANGE_USER": "Please change the user",
    "GOOD_BYE": "Good bye!",
    "NO_USERS": "There are no users",
    "HELLO": "How can I help you?",
}

SERIALIZER_PATH = "addressbook.pkl"


def input_error(func):
    """
    Decorator to handle input errors.
    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except (ValueError, TypeError, IndexError, KeyError) as e:
            return str(e)

    return wrapper


def serializes(func, object, serializer=None):
    """
    Decorator to serialize the address book.

    Args:
        func (Callable): The function to decorate.
        object (Any): The object to serialize.
        serializer (AddressBookSerializer | None): The serializer to use.

    Returns:
        Callable: The decorated function.
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
    Parse the input.

    Args:
        line (str): The line to parse.

    Returns:
        tuple[str, list[str]]: A tuple containing the command and the arguments.
    """
    if line.strip() == "":
        return "", []
    arguments = line.split()
    return arguments[0].lower(), arguments[1:]


@input_error
def hello(_: AddressBook, arguments: list[str] = []) -> str:
    """
    Print the hello message.

    Args:
        _ (AddressBook): The book of contacts.
        arguments (list[str]): The arguments to the hello command.

    Returns:
        str: The hello message.
    """
    if arguments:
        raise ValueError(COMMAND_MESSAGES["INVALID_COMMAND"])

    return COMMAND_MESSAGES["HELLO"]


@input_error
def add_contact(book: AddressBook, arguments: list[str]) -> str:
    """
    Add a new contact.

    Args:
        book (AddressBook): The book of contacts.
        arguments (list[str]): The arguments to add the contact.

    Returns:
        str: The response to the command.
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
def update_contact(book: AddressBook, arguments: list[str]) -> str:
    """
    Update a contact.

    Args:
        book (AddressBook): The book of contacts.
        arguments (list[str]): The arguments to update the contact.

    Returns:
        str: The response to the command.

    Notes:
        Replaces all the phones the user has with the current phone.
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
    Add a birthday to a contact.

    Args:
        book (AddressBook): The book of contacts.
        arguments (list[str]): The arguments to add the birthday to the contact.

    Returns:
        str: The response to the command.
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
    Show the birthday of a contact.

    Args:
        book (AddressBook): The book of contacts.
        arguments (list[str]): The arguments to show the birthday of the contact.

    Returns:
        str: The response to the command.
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
    Show the phone number of a contact.

    Args:
        book (AddressBook): The book of contacts.
        arguments (list[str]): The arguments to show the phone number of the contact.

    Returns:
        str: The response to the command.
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
    Show the birthdays of the contacts.

    Args:
        book (AddressBook): The book of contacts.
        arguments (list[str]): The arguments to show the birthdays.

    Returns:
        str: The response to the command.
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
    Show all contacts.

    Args:
        book (AddressBook): The book of contacts.
        arguments (list[str]): The arguments to show all contacts.

    Returns:
        str: The response to the command.
    """
    if arguments:
        raise ValueError(COMMAND_MESSAGES["INVALID_COMMAND"])
    if not book.data:
        raise ValueError(COMMAND_MESSAGES["NO_USERS"])

    count_users = len(book.data)
    users_list = [
        f"{record.name}: {'; '.join(phone.value for phone in record.phones)}"
        for _, record in sorted(book.data.items())
    ]
    return f"Stored users ({count_users}):\n{'\n'.join(users_list)}"


@input_error
def exit(_: AddressBook, arguments: list[str] = []) -> str:
    """
    Exit the program.

    Args:
        _ (AddressBook): The book of contacts.
        arguments (list[str], optional): The arguments to the exit command. Defaults to [].

    Returns:
        str: The goodbye message.
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
    Handle the command.

    Args:
        command (str): The command to handle.
        arguments (list[str]): The arguments to the command.
        book (AddressBook): The book of contacts.

    Returns:
        str: The response to the command.
    """
    commands = {
        "hello": hello,
        "add": serializes(add_contact, book, serializer),
        "update": serializes(update_contact, book, serializer),
        "phone": show_phone,
        "all": show_all,
        "add-birthday": serializes(add_birthday, book, serializer),
        "show-birthday": show_birthday,
        "birthdays": birthdays,
        "exit": exit,
        "close": exit,
    }

    if command not in commands:
        return COMMAND_MESSAGES["INVALID_COMMAND"]

    return commands[command](book, arguments)


def main() -> None:
    """
    Main function.
    """
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
