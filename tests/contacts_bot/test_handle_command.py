import pytest
import time_machine

from src.scripts.contacts_bot import COMMAND_MESSAGES, handle_command


@pytest.mark.parametrize(
    "command,arguments,expected",
    [
        ("hello", [], COMMAND_MESSAGES["HELLO"]),
        ("hello", ["extra"], COMMAND_MESSAGES["INVALID_COMMAND"]),
        ("not_a_command", [], COMMAND_MESSAGES["INVALID_COMMAND"]),
    ],
)
def test_handle_command_hello_and_unknown(command, arguments, expected):
    """Перевіряє hello, невалідну арність і невідому команду.

    Дано:
        Параметризована команда та аргументи (hello, зайві аргументи або невідома команда).
    Коли:
        Викликається ``handle_command``.
    Тоді:
        Повертається очікуване привітання або ``Invalid command.``.

    Args:
        command: Назва команди.
        arguments: Аргументи команди.
        expected: Очікувана відповідь.
    """
    assert handle_command({}, command, arguments) == expected


def test_handle_command_add_and_update_via_dispatch(
    empty_address_book, valid_phone_generator
):
    """Перевіряє add і update через диспетчер команд."""
    gen = valid_phone_generator

    phone1 = gen()
    assert (
        handle_command(empty_address_book, "add", ["x", phone1])
        == COMMAND_MESSAGES["CONTACT_ADDED"]
    )

    phone2 = gen()
    assert (
        handle_command(empty_address_book, "add", ["x", phone2])
        == COMMAND_MESSAGES["CONTACT_ADDED"]
    )

    last_phone = gen()
    print(f"DEBUG: {phone1=} {phone2=} {last_phone=}")

    assert (
        handle_command(empty_address_book, "update", ["x", last_phone])
        == COMMAND_MESSAGES["CONTACT_UPDATED"]
    )
    assert empty_address_book.data["x"].phones[-1].value == last_phone


def test_handle_command_add_birthday_via_dispatch(
    book_with_contact, valid_birthday_str
):
    """Перевіряє add-birthday через handle_command.

    Дано:
        Контакт у книзі.
    Коли:
        Диспетчеризується ``add-birthday``.
    Тоді:
        Повідомлення про додавання ДН, дата зберігається.

    Args:
        book_with_contact: Книга з контактом.
        valid_birthday_str: Валідна дата.
    """
    assert handle_command(
        book_with_contact, "add-birthday", ["JohnDoe", valid_birthday_str]
    ) == COMMAND_MESSAGES["BIRTHDAY_ADDED"].format(
        old_birthday=None, new_birthday=valid_birthday_str, name="JohnDoe"
    )
    assert book_with_contact.data["JohnDoe"].birthday.value == valid_birthday_str


def test_handle_command_show_birthday_via_dispatch(
    book_with_contact, valid_birthday_str
):
    """Перевіряє show-birthday через handle_command.

    Дано:
        Контакт із ДН, встановленим через ``handle_command``.
    Коли:
        Диспетчеризується ``show-birthday``.
    Тоді:
        Повертається відформатоване повідомлення з датою.

    Args:
        book_with_contact: Книга з контактом.
        valid_birthday_str: Валідна дата.
    """
    handle_command(book_with_contact, "add-birthday", ["JohnDoe", valid_birthday_str])

    assert handle_command(
        book_with_contact, "show-birthday", ["JohnDoe"]
    ) == COMMAND_MESSAGES["BIRTHDAY_SHOWED"].format(
        name="JohnDoe", birthday=valid_birthday_str
    )


def test_handle_command_birthdays_via_dispatch(empty_address_book):
    """Перевіряє birthdays через handle_command.

    Дано:
        Контакт із найближчим ДН на зафіксованій даті (2026-05-19).
    Коли:
        Диспетчеризується ``birthdays``.
    Тоді:
        У виводі є відформатований рядок найближчого ДН.

    Args:
        empty_address_book: Книга, наповнена під час тесту.
    """
    with time_machine.travel("2026-05-19"):
        handle_command(empty_address_book, "add", ["Alice", "1234567890"])
        handle_command(empty_address_book, "add-birthday", ["Alice", "20.05.1990"])

        assert "20.05.2026 (Wednesday) Alice" in handle_command(
            empty_address_book, "birthdays", []
        )


@pytest.mark.parametrize(
    "command,arguments,expected",
    [
        ("add", ["onlyone"], COMMAND_MESSAGES["INVALID_COMMAND"]),
        ("update", ["x"], COMMAND_MESSAGES["INVALID_COMMAND"]),
        ("add-birthday", ["x"], COMMAND_MESSAGES["INVALID_COMMAND"]),
        ("show-birthday", [], COMMAND_MESSAGES["INVALID_COMMAND"]),
        ("birthdays", ["extra"], COMMAND_MESSAGES["INVALID_COMMAND"]),
        ("phone", [], COMMAND_MESSAGES["INVALID_COMMAND"]),
        ("all", ["extra"], COMMAND_MESSAGES["INVALID_COMMAND"]),
    ],
)
def test_handle_command_wrong_arity(empty_address_book, command, arguments, expected):
    """Перевіряє невалідну кількість аргументів для команд.

    Дано:
        Адресна книга та параметризовані команди з некоректною арністю.
    Коли:
        Викликається ``handle_command``.
    Тоді:
        Повертається ``Invalid command.``.

    Args:
        empty_address_book: Адресна книга.
        command: Назва команди.
        arguments: Аргументи команди.
        expected: Очікувана відповідь.
    """
    assert handle_command(empty_address_book, command, arguments) == expected


@pytest.mark.parametrize(
    "command,arguments,expected",
    [
        ("", [], COMMAND_MESSAGES["INVALID_COMMAND"]),
        ("  ", [], COMMAND_MESSAGES["INVALID_COMMAND"]),
    ],
)
def test_handle_command_empty_line_invalid(
    empty_address_book, command, arguments, expected
):
    """Перевіряє порожню або пробільну команду.

    Дано:
        Порожній або пробільний рядок команди.
    Коли:
        Викликається ``handle_command``.
    Тоді:
        Повертається ``Invalid command.``.

    Args:
        empty_address_book: Адресна книга.
        command: Рядок команди.
        arguments: Аргументи.
        expected: Очікувана відповідь.
    """
    assert handle_command(empty_address_book, command, arguments) == expected


def test_handle_command_phone_no_user(empty_address_book):
    """Перевіряє phone для відсутнього користувача.

    Дано:
        Порожня адресна книга.
    Коли:
        Диспетчеризується ``phone`` для неіснуючого імені.
    Тоді:
        Повертається ``No such user``.

    Args:
        empty_address_book: Порожня книга.
    """
    assert (
        handle_command(empty_address_book, "phone", ["Ghost"])
        == COMMAND_MESSAGES["NO_SUCH_USER"]
    )


def test_handle_command_update_no_user(empty_address_book, valid_phone):
    """Перевіряє update для відсутнього користувача.

    Дано:
        Порожня адресна книга.
    Коли:
        Диспетчеризується ``update`` для неіснуючого імені.
    Тоді:
        Повертається ``No such user``.

    Args:
        empty_address_book: Порожня книга.
        valid_phone: Валідний номер.
    """
    assert (
        handle_command(empty_address_book, "update", ["Ghost", valid_phone])
        == COMMAND_MESSAGES["NO_SUCH_USER"]
    )


def test_handle_command_exit_close_returns_none(empty_address_book):
    """Перевіряє команди exit і close.

    Дано:
        Адресна книга.
    Коли:
        Диспетчеризуються ``exit`` або ``close``.
    Тоді:
        Повертається прощальне повідомлення, книга не змінюється.

    Args:
        empty_address_book: Адресна книга.
    """
    assert (
        handle_command(empty_address_book, "exit", []) == COMMAND_MESSAGES["GOOD_BYE"]
    )
    assert (
        handle_command(empty_address_book, "close", []) == COMMAND_MESSAGES["GOOD_BYE"]
    )
    assert len(empty_address_book.data) == 0
