from src.scripts.contacts_bot import COMMAND_MESSAGES, update_contact
from tests.contacts_bot.shared import RECORD_ERRORS


def test_change_contact_updates(book_with_contact, valid_phone):
    """Перевіряє оновлення телефону контакту.

    Дано:
        Адресна книга з наявним контактом.
    Коли:
        ``update_contact`` викликається з новим валідним номером.
    Тоді:
        Повертається повідомлення про оновлення, новий номер зберігається.

    Args:
        book_with_contact: Книга з JohnDoe.
        valid_phone: Новий валідний номер.
    """
    assert (
        update_contact(book_with_contact, ["JohnDoe", valid_phone])
        == COMMAND_MESSAGES["CONTACT_UPDATED"]
    )
    assert any(
        phone.value == valid_phone for phone in book_with_contact.data["JohnDoe"].phones
    )


def test_change_contact_no_such_user(empty_address_book, valid_phone):
    """Перевіряє update для відсутнього користувача.

    Дано:
        Порожня адресна книга.
    Коли:
        ``update_contact`` викликається для неіснуючого імені.
    Тоді:
        Повертається ``No such user``, книга лишається порожньою.

    Args:
        empty_address_book: Порожня книга.
        valid_phone: Валідний номер.
    """
    assert (
        update_contact(empty_address_book, ["Nobody", valid_phone])
        == COMMAND_MESSAGES["NO_SUCH_USER"]
    )
    assert len(empty_address_book.data) == 0


def test_change_contact_invalid_credentials(book_with_contact, valid_phone):
    """Перевіряє update з невалідним номером.

    Дано:
        Контакт із валідним телефоном.
    Коли:
        ``update_contact`` викликається з невалідним рядком номера.
    Тоді:
        Повертається помилка валідації, початковий номер зберігається.

    Args:
        book_with_contact: Книга з контактом.
        valid_phone: Початковий валідний номер.
    """
    assert (
        update_contact(book_with_contact, ["JohnDoe", "abcdefghijkl"])
        == RECORD_ERRORS["PHONE_NOT_VALID"]
    )
    assert any(
        phone.value == valid_phone for phone in book_with_contact.data["JohnDoe"].phones
    )


def test_change_contact_with_multiple_phones_is_not_allowed(
    book_with_contact, valid_phone_generator
):
    """Перевіряє заборону кількох нових номерів у update.

    Дано:
        Наявний контакт.
    Коли:
        ``update_contact`` викликається з більш ніж одним новим номером.
    Тоді:
        Повертається ``Invalid command.``.

    Args:
        book_with_contact: Книга з контактом.
        valid_phone_generator: Генератор валідних номерів.
    """
    valid_phones = [valid_phone_generator() for _ in range(3)]
    assert (
        update_contact(book_with_contact, ["JohnDoe", *valid_phones])
        == COMMAND_MESSAGES["INVALID_COMMAND"]
    )
