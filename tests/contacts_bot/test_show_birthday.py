import pytest

from src.scripts.contacts_bot import COMMAND_MESSAGES, add_birthday, show_birthday


def test_show_birthday_returns_existing_birthday(book_with_contact, valid_birthday_str):
    """Перевіряє показ дня народження після add_birthday.

    Дано:
        Контакт із днем народження, доданим через ``add_birthday``.
    Коли:
        Викликається ``show_birthday``.
    Тоді:
        Повертається відформатоване повідомлення з датою.

    Args:
        book_with_contact: Книга з контактом.
        valid_birthday_str: Валідна дата.
    """
    add_birthday(book_with_contact, ["JohnDoe", valid_birthday_str])

    assert show_birthday(book_with_contact, ["JohnDoe"]) == COMMAND_MESSAGES[
        "BIRTHDAY_SHOWED"
    ].format(name="JohnDoe", birthday=valid_birthday_str)


def test_show_birthday_reads_record_stored_in_address_book(
    book_with_contact, valid_birthday_str
):
    """Перевіряє показ ДН, встановленого напряму на записі.

    Дано:
        День народження встановлено безпосередньо на записі в книзі.
    Коли:
        Викликається ``show_birthday``.
    Тоді:
        Повертається відформатоване повідомлення з датою.

    Args:
        book_with_contact: Книга з контактом.
        valid_birthday_str: Валідна дата.
    """
    record = book_with_contact.data["JohnDoe"]
    record.add_birthday(valid_birthday_str)

    assert show_birthday(book_with_contact, ["JohnDoe"]) == COMMAND_MESSAGES[
        "BIRTHDAY_SHOWED"
    ].format(name="JohnDoe", birthday=valid_birthday_str)


def test_show_birthday_no_such_user(empty_address_book):
    """Перевіряє show_birthday для відсутнього користувача.

    Дано:
        Порожня адресна книга.
    Коли:
        ``show_birthday`` викликається для неіснуючого імені.
    Тоді:
        Повертається ``No such user``.

    Args:
        empty_address_book: Порожня книга.
    """
    assert (
        show_birthday(empty_address_book, ["Nobody"])
        == COMMAND_MESSAGES["NO_SUCH_USER"]
    )


def test_show_birthday_no_birthday(book_with_contact):
    """Перевіряє show_birthday без встановленого ДН.

    Дано:
        Контакт без дня народження.
    Коли:
        Викликається ``show_birthday``.
    Тоді:
        Повертається повідомлення про відсутність ДН.

    Args:
        book_with_contact: Книга з контактом без ДН.
    """
    assert show_birthday(book_with_contact, ["JohnDoe"]) == COMMAND_MESSAGES[
        "NO_BIRTHDAY_SET"
    ].format(name="JohnDoe")


@pytest.mark.parametrize(
    "arguments",
    [
        [],
        ["JohnDoe", "extra"],
    ],
)
def test_show_birthday_wrong_arity(book_with_contact, arguments):
    """Перевіряє невалідну кількість аргументів show_birthday.

    Дано:
        Контакт у книзі та параметризовані некоректні аргументи.
    Коли:
        Викликається ``show_birthday``.
    Тоді:
        Повертається ``Invalid command.``.

    Args:
        book_with_contact: Книга з контактом.
        arguments: Аргументи команди.
    """
    assert (
        show_birthday(book_with_contact, arguments)
        == COMMAND_MESSAGES["INVALID_COMMAND"]
    )
