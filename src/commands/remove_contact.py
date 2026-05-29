from src.address_book import AddressBook
from src.utils.decorators.input_error import input_error
from src.messages import REMOVE_CONTACT_MESSAGES


def try_remove_contact(book: AddressBook, name: str) -> str:
    """
    Видаляє телефон з запису.

    Аргументи:
        book: Адресна книга.
        name: Ім'я контакту.

    Винятки:
        KeyError: Якщо контакт не знайдено.

    Повертає:
        str: Відповідь на команду.
    """
    if not book.remove_record(name):
        raise KeyError(
            REMOVE_CONTACT_MESSAGES["CONTACT_NOT_FOUND"].format(name=name))
    return REMOVE_CONTACT_MESSAGES["CONTACT_REMOVED"].format(name=name)


@input_error
def remove_contact(book: AddressBook, arguments: list[str]) -> str:
    """
    Видаляє контакт з адресної книги.

    Аргументи:
        book (AddressBook): Адресна книга.
        arguments (list[str]): Ім'я контакту.
    """
    if not 1 <= len(arguments) <= 2:
        raise ValueError(REMOVE_CONTACT_MESSAGES["INVALID_SYNTAX"])
    name = arguments[0]
    record = book.find_record(name)
    if not record:
        raise KeyError(
            REMOVE_CONTACT_MESSAGES["CONTACT_NOT_FOUND"].format(name=name))

    if len(arguments) == 2:
        phone = arguments[1]
    else:
        return try_remove_contact(book, name)

    if not record.remove_phone(phone):
        raise KeyError(
            REMOVE_CONTACT_MESSAGES["PHONE_NOT_FOUND"].format(phone=phone,
                                                              name=name)
            )
    return REMOVE_CONTACT_MESSAGES["PHONE_REMOVED"].format(phone=phone,
                                                           name=name)
