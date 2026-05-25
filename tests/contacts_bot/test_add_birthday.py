import pytest

from src.scripts.contacts_bot import COMMAND_MESSAGES, add_birthday

from .shared import RECORD_ERRORS


def test_add_birthday_adds_to_existing_record(book_with_contact, valid_birthday_str):
    """Перевіряє додавання дня народження до контакту.

    Дано:
        Контакт без дня народження.
    Коли:
        Викликається ``add_birthday`` з валідною датою.
    Тоді:
        Повертається повідомлення про додавання, дата зберігається.

    Args:
        book_with_contact: Книга з контактом JohnDoe.
        valid_birthday_str: Валідна дата DD.MM.YYYY.
    """
    assert add_birthday(
        book_with_contact, ["JohnDoe", valid_birthday_str]
    ) == COMMAND_MESSAGES["BIRTHDAY_ADDED"].format(
        old_birthday=None, new_birthday=valid_birthday_str, name="JohnDoe"
    )
    assert book_with_contact.data["JohnDoe"].birthday.value == valid_birthday_str


def test_add_birthday_edits_record_stored_in_address_book(
    book_with_contact, valid_birthday_str
):
    """Перевіряє оновлення того самого об'єкта запису в книзі.

    Дано:
        Посилання на запис контакту в книзі.
    Коли:
        Викликається ``add_birthday``.
    Тоді:
        Той самий об'єкт запису в книзі отримує день народження.

    Args:
        book_with_contact: Книга з контактом.
        valid_birthday_str: Валідна дата.
    """
    record = book_with_contact.data["JohnDoe"]

    assert add_birthday(
        book_with_contact, ["JohnDoe", valid_birthday_str]
    ) == COMMAND_MESSAGES["BIRTHDAY_ADDED"].format(
        old_birthday=None, new_birthday=valid_birthday_str, name="JohnDoe"
    )

    assert book_with_contact.data["JohnDoe"] is record
    assert record.birthday.value == valid_birthday_str


def test_add_birthday_no_such_user(empty_address_book, valid_birthday_str):
    """Перевіряє додавання ДН для відсутнього користувача.

    Дано:
        Порожня адресна книга.
    Коли:
        ``add_birthday`` викликається для неіснуючого імені.
    Тоді:
        Повертається ``No such user``, книга лишається порожньою.

    Args:
        empty_address_book: Порожня книга.
        valid_birthday_str: Валідна дата.
    """
    assert (
        add_birthday(empty_address_book, ["Nobody", valid_birthday_str])
        == COMMAND_MESSAGES["NO_SUCH_USER"]
    )
    assert len(empty_address_book.data) == 0


def test_add_birthday_invalid_birthday(book_with_contact, invalid_birthday_str):
    """Перевіряє відхилення невалідної дати.

    Дано:
        Контакт без дня народження.
    Коли:
        ``add_birthday`` викликається з невалідною датою.
    Тоді:
        Повертається помилка валідації, ``birthday`` лишається ``None``.

    Args:
        book_with_contact: Книга з контактом.
        invalid_birthday_str: Невалідна дата.
    """
    assert add_birthday(
        book_with_contact, ["JohnDoe", invalid_birthday_str]
    ) == RECORD_ERRORS["BIRTHDAY_NOT_VALID"].format(birthday=invalid_birthday_str)
    assert book_with_contact.data["JohnDoe"].birthday is None


def test_add_birthday_replaces_existing_birthday(
    book_with_contact, valid_birthday_str, new_valid_birthday_str
):
    """Перевіряє заміну існуючого дня народження.

    Дано:
        Контакт, у якого вже є день народження.
    Коли:
        ``add_birthday`` викликається з новою валідною датою.
    Тоді:
        Повідомлення містить стару й нову дати, дата замінюється.

    Args:
        book_with_contact: Книга з контактом.
        valid_birthday_str: Початкова дата.
        new_valid_birthday_str: Нова дата.
    """
    add_birthday(book_with_contact, ["JohnDoe", valid_birthday_str])

    assert add_birthday(
        book_with_contact, ["JohnDoe", new_valid_birthday_str]
    ) == COMMAND_MESSAGES["BIRTHDAY_ADDED"].format(
        old_birthday=valid_birthday_str,
        new_birthday=new_valid_birthday_str,
        name="JohnDoe",
    )
    assert book_with_contact.data["JohnDoe"].birthday.value == new_valid_birthday_str


@pytest.mark.parametrize(
    "arguments",
    [
        [],
        ["JohnDoe"],
        ["JohnDoe", "invalid", "invalid"],
    ],
)
def test_add_birthday_wrong_arity(book_with_contact, arguments):
    """Перевіряє невалідну кількість аргументів.

    Дано:
        Контакт у книзі та параметризовані некоректні аргументи.
    Коли:
        Викликається ``add_birthday``.
    Тоді:
        Повертається ``Invalid command.``.

    Args:
        book_with_contact: Книга з контактом.
        arguments: Аргументи команди.
    """
    assert (
        add_birthday(book_with_contact, arguments)
        == COMMAND_MESSAGES["INVALID_COMMAND"]
    )
