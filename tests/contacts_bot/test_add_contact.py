import pytest

from src.scripts.contacts_bot import COMMAND_MESSAGES, add_contact
from tests.contacts_bot.shared import INVALID_PHONE_12, RECORD_ERRORS


def test_add_contact_inserts_and_message(empty_address_book, valid_phone):
    """Перевіряє додавання нового контакту.

    Дано:
        Порожня адресна книга та валідні ім'я і телефон.
    Коли:
        Викликається ``add_contact``.
    Тоді:
        Повертається повідомлення про успіх і зберігається один контакт.

    Args:
        empty_address_book: Порожня книга.
        valid_phone: Валідний номер телефону.
    """
    assert (
        add_contact(empty_address_book, ["Zoe", valid_phone])
        == COMMAND_MESSAGES["CONTACT_ADDED"]
    )
    assert len(empty_address_book.data) == 1


def test_add_contact_duplicate_phones(empty_address_book, valid_phone):
    """Перевіряє заборону дублювання телефону.

    Дано:
        Контакт, у якого вже є цей телефон.
    Коли:
        ``add_contact`` викликається знову з тим самим номером.
    Тоді:
        Повертається помилка дубліката, залишається один контакт.

    Args:
        empty_address_book: Книга з одним контактом.
        valid_phone: Номер, який уже додано.
    """
    assert (
        add_contact(empty_address_book, ["Zoe", valid_phone])
        == COMMAND_MESSAGES["CONTACT_ADDED"]
    )
    assert (
        add_contact(empty_address_book, ["Zoe", valid_phone])
        == RECORD_ERRORS["PHONE_ALREADY_EXISTS"]
    )
    assert len(empty_address_book.data) == 1


@pytest.mark.parametrize(
    "arguments,expected",
    [
        (["bad"], COMMAND_MESSAGES["INVALID_COMMAND"]),
        (["bad", "1234567890", "1234567890"], COMMAND_MESSAGES["INVALID_COMMAND"]),
        (["bad", "name", INVALID_PHONE_12], COMMAND_MESSAGES["INVALID_COMMAND"]),
        (["bad name", "12345678901"], RECORD_ERRORS["NAME_NOT_VALID"]),
        (["Good", "+1234567890123456"], RECORD_ERRORS["PHONE_NOT_VALID"]),
    ],
)
def test_add_contact_invalid_name_or_phone(empty_address_book, arguments, expected):
    """Перевіряє помилки при невалідних аргументах add.

    Дано:
        Порожня книга та параметризовані невалідні аргументи.
    Коли:
        Викликається ``add_contact``.
    Тоді:
        Повертається очікуване повідомлення про помилку, книга порожня.

    Args:
        empty_address_book: Порожня адресна книга.
        arguments: Аргументи команди.
        expected: Очікуване повідомлення.
    """
    assert add_contact(empty_address_book, arguments) == expected
    assert len(empty_address_book.data) == 0


@pytest.fixture
def add_contact_fixture(valid_phone):
    return ["JohnDoe", valid_phone]


@pytest.mark.parametrize("add_contact_fixture", [i for i in range(10)], indirect=True)
def test_add_valid_name_and_phone(empty_address_book, add_contact_fixture):
    """Перевіряє стабільність додавання валідного контакту.

    Дано:
        Порожня книга та валідні аргументи (10 параметризованих запусків).
    Коли:
        Викликається ``add_contact``.
    Тоді:
        Повертається успіх і один телефон зберігається для JohnDoe.

    Args:
        empty_address_book: Порожня адресна книга.
        add_contact_fixture: Ім'я та телефон для додавання.
    """
    assert (
        add_contact(empty_address_book, add_contact_fixture)
        == COMMAND_MESSAGES["CONTACT_ADDED"]
    )
    assert len(empty_address_book.data) == 1
    assert len(empty_address_book.data["JohnDoe"].phones) == 1


def test_add_multiple_phones(empty_address_book, valid_phone_generator):
    """Перевіряє додавання кількох телефонів одному контакту.

    Дано:
        Порожня адресна книга.
    Коли:
        ``add_contact`` викликається тричі для одного імені з різними номерами.
    Тоді:
        Кожен виклик успішний, у контакту три телефони.

    Args:
        empty_address_book: Порожня адресна книга.
        valid_phone_generator: Генератор валідних номерів.
    """
    valid_phones = [valid_phone_generator() for _ in range(3)]
    for phone in valid_phones:
        assert (
            add_contact(empty_address_book, ["JohnDoe", phone])
            == COMMAND_MESSAGES["CONTACT_ADDED"]
        )
    assert len(empty_address_book.data) == 1
    assert all(
        phone.value in valid_phones
        for phone in empty_address_book.data["JohnDoe"].phones
    )
