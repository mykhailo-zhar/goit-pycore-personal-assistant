from src.address_book import AddressBook
from src.utils.decorators.input_error import input_error

INSERT_EMAIL_MESSAGES = {
    "INVALID_SYNTAX": "Invalid syntax. Usage: insert-email <name> <email>",
    "NO_SUCH_USER": "No such user",
    "EMAIL_ADDED": "Email added: {email} for {name}",
    "EMAIL_REPLACED": "Email replaced: {old_email} with {new_email} for {name}",
    "EMAIL_NOT_VALID": "Email is not valid",
}


@input_error
def insert_email(book: AddressBook, arguments: list[str]) -> str:
    """
    Додає день народження контакту.

    Аргументи:
        book (AddressBook): Адресна книга.
        arguments (list[str]): Ім'я та дата DD.MM.YYYY.

    Повертає:
        str: Відповідь на команду.
    """
    if len(arguments) != 2:
        raise ValueError(INSERT_EMAIL_MESSAGES["INVALID_SYNTAX"])
    name, email = arguments

    record = book.find_record(name)

    if not record:
        raise ValueError(INSERT_EMAIL_MESSAGES["NO_SUCH_USER"])

    old_value = record.email.value if record.email else None

    record.email = email
    if old_value:
        return INSERT_EMAIL_MESSAGES["EMAIL_REPLACED"].format(
            old_email=old_value,
            new_email=email,
            name=name,
        )

    return INSERT_EMAIL_MESSAGES["EMAIL_ADDED"].format(
        email=email,
        name=name,
    )
