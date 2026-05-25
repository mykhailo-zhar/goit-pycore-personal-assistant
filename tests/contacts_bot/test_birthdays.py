import pytest
import time_machine

from src.scripts.contacts_bot import (
    COMMAND_MESSAGES,
    add_birthday,
    add_contact,
    birthdays,
)


def test_birthdays_empty_address_book(empty_address_book):
    """
    Given an empty address book
    When birthdays is called with no arguments
    Then the no-users message is returned
    """
    assert birthdays(empty_address_book, []) == COMMAND_MESSAGES["NO_USERS"]


def test_birthdays_prints_upcoming_birthdays_per_line(empty_address_book):
    """
    Given contacts with upcoming birthdays on a frozen date (2026-05-19)
    When birthdays is called
    Then the header and formatted lines for Alice and Bob appear in the output
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
    """
    Given an address book and extra arguments to birthdays
    When birthdays is called
    Then the invalid-command message is returned
    """
    assert (
        birthdays(empty_address_book, arguments) == COMMAND_MESSAGES["INVALID_COMMAND"]
    )
