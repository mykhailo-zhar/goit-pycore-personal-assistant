from src.scripts.contacts_bot import COMMAND_MESSAGES, update_contact
from tests.contacts_bot.shared import RECORD_ERRORS


def test_change_contact_updates_first_phone(
    book_with_contact, valid_phone, valid_phone_generator
):
    """Перевіряє оновлення першого телефону контакту (2 аргументи).

    Дано:
        Адресна книга з наявним контактом.
    Коли:
        ``update_contact`` викликається з новим валідним номером (без старого).
    Тоді:
        Повертається повідомлення про оновлення, новий номер зберігається.
    """
    new_phone = valid_phone_generator()
    assert (
        update_contact(book_with_contact, ["JohnDoe", new_phone])
        == COMMAND_MESSAGES["CONTACT_UPDATED"]
    )
    assert any(
        phone.value == new_phone for phone in book_with_contact.data["JohnDoe"].phones
    )


def test_change_contact_updates_specific_phone(
    book_with_contact, valid_phone, valid_phone_generator
):
    """Перевіряє заміну конкретного телефону (3 аргументи).

    Дано:
        Адресна книга з наявним контактом і відомим номером.
    Коли:
        ``update_contact`` викликається зі старим і новим номером.
    Тоді:
        Повертається повідомлення про оновлення, новий номер зберігається.
    """
    new_phone = valid_phone_generator()
    assert (
        update_contact(book_with_contact, ["JohnDoe", valid_phone, new_phone])
        == COMMAND_MESSAGES["CONTACT_UPDATED"]
    )
    assert any(
        phone.value == new_phone for phone in book_with_contact.data["JohnDoe"].phones
    )


def test_change_contact_no_such_user(empty_address_book, valid_phone):
    """Перевіряє update для відсутнього користувача.

    Дано:
        Порожня адресна книга.
    Коли:
        ``update_contact`` викликається для неіснуючого імені.
    Тоді:
        Повертається ``No such user``, книга лишається порожньою.
    """
    assert (
        update_contact(empty_address_book, ["Nobody", valid_phone])
        == COMMAND_MESSAGES["NO_SUCH_USER"]
    )
    assert len(empty_address_book.data) == 0


def test_change_contact_invalid_new_phone(book_with_contact, valid_phone):
    """Перевіряє update з невалідним новим номером (3 аргументи).

    Дано:
        Контакт із валідним телефоном.
    Коли:
        ``update_contact`` викликається з невалідним новим номером.
    Тоді:
        Повертається помилка валідації, початковий номер зберігається.
    """
    assert (
        update_contact(book_with_contact, ["JohnDoe", valid_phone, "abcdefghijkl"])
        == RECORD_ERRORS["PHONE_NOT_VALID"]
    )
    assert any(
        phone.value == valid_phone for phone in book_with_contact.data["JohnDoe"].phones
    )


def test_change_contact_invalid_old_phone(
    book_with_contact, valid_phone, valid_phone_generator
):
    """Перевіряє update з невалідним старим номером (3 аргументи).

    Дано:
        Контакт із валідним телефоном.
    Коли:
        ``update_contact`` викликається зі старим номером якого не існує.
    Тоді:
        Повертається помилка про відсутність номера.
    """
    new_phone = valid_phone_generator()
    assert (
        update_contact(book_with_contact, ["JohnDoe", "0000000000", new_phone])
        == RECORD_ERRORS["PHONE_NOT_FOUND"]
    )


def test_change_contact_with_multiple_phones_is_not_allowed(
    book_with_contact, valid_phone_generator
):
    """Перевіряє заборону 4+ аргументів у update.

    Дано:
        Наявний контакт.
    Коли:
        ``update_contact`` викликається з 4 і більше аргументами.
    Тоді:
        Повертається ``Invalid command.``.
    """
    valid_phones = [valid_phone_generator() for _ in range(3)]
    assert (
        update_contact(book_with_contact, ["JohnDoe", *valid_phones])
        == COMMAND_MESSAGES["INVALID_COMMAND"]
    )
