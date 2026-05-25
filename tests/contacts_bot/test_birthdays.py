import pytest
import time_machine

from src.scripts.contacts_bot import (
    COMMAND_MESSAGES,
    add_birthday,
    add_contact,
    birthdays,
)


def test_birthdays_empty_address_book(empty_address_book):
    """Перевіряє команду birthdays для порожньої книги.

    Дано:
        Порожня адресна книга.
    Коли:
        Викликається ``birthdays`` без аргументів.
    Тоді:
        Повертається повідомлення про відсутність користувачів.

    Args:
        empty_address_book: Порожня книга.
    """
    assert birthdays(empty_address_book, []) == COMMAND_MESSAGES["NO_USERS"]


def test_birthdays_prints_upcoming_birthdays_per_line(empty_address_book):
    """Перевіряє вивід найближчих днів народження.

    Дано:
        Контакти з ДН на зафіксованій даті (2026-05-19).
    Коли:
        Викликається ``birthdays``.
    Тоді:
        У виводі заголовок і рядки для Alice та Bob.

    Args:
        empty_address_book: Книга, наповнена під час тесту.
    """
    with time_machine.travel("2026-05-19"):
        add_contact(empty_address_book, ["Alice", "1234567890"])
        add_birthday(empty_address_book, ["Alice", "20.05.1990"])
        add_contact(empty_address_book, ["Bob", "1234567891"])
        add_birthday(empty_address_book, ["Bob", "21.05.1991"])
        add_contact(empty_address_book, ["Charlie", "1234567892"])

        out = birthdays(empty_address_book, [])

        assert "Upcoming birthdays:" in out
        assert all(
            line in out
            for line in [
                "20.05.2026 (Wednesday) Alice",
                "21.05.2026 (Thursday) Bob",
            ]
        )


@pytest.mark.parametrize(
    "arguments",
    [
        ["extra"],
    ],
)
def test_birthdays_wrong_arity(empty_address_book, arguments):
    """Перевіряє зайві аргументи команди birthdays.

    Дано:
        Адресна книга та зайві аргументи.
    Коли:
        Викликається ``birthdays``.
    Тоді:
        Повертається ``Invalid command.``.

    Args:
        empty_address_book: Адресна книга.
        arguments: Зайві аргументи.
    """
    assert (
        birthdays(empty_address_book, arguments) == COMMAND_MESSAGES["INVALID_COMMAND"]
    )
