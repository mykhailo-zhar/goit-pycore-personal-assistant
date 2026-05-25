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
    """
    Given a parametrized command and arguments (hello, invalid arity, or unknown)
    When handle_command is dispatched
    Then the expected hello or invalid-command message is returned
    """
    assert handle_command({}, command, arguments) == expected


def test_handle_command_add_and_update_via_dispatch(
    empty_address_book, valid_phone_generator
):
    """
    Given an empty address book
    When add is called twice for the same name then update with a new phone
    Then added/updated messages are returned and the last phone is stored
    """
    assert (
        handle_command(empty_address_book, "add", ["x", valid_phone_generator()])
        == COMMAND_MESSAGES["CONTACT_ADDED"]
    )
    assert (
        handle_command(empty_address_book, "add", ["x", valid_phone_generator()])
        == COMMAND_MESSAGES["CONTACT_ADDED"]
    )
    last_valid_phone = valid_phone_generator()
    assert (
        handle_command(empty_address_book, "update", ["x", last_valid_phone])
        == COMMAND_MESSAGES["CONTACT_UPDATED"]
    )
    assert empty_address_book.data["x"].phones[-1].value == last_valid_phone


def test_handle_command_add_birthday_via_dispatch(
    book_with_contact, valid_birthday_str
):
    """
    Given a contact in the book
    When add-birthday is dispatched via handle_command
    Then the birthday-added message is returned and the date is stored
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
    """
    Given a contact with a birthday set via handle_command
    When show-birthday is dispatched
    Then the formatted birthday message is returned
    """
    handle_command(book_with_contact, "add-birthday", ["JohnDoe", valid_birthday_str])

    assert handle_command(
        book_with_contact, "show-birthday", ["JohnDoe"]
    ) == COMMAND_MESSAGES["BIRTHDAY_SHOWED"].format(
        name="JohnDoe", birthday=valid_birthday_str
    )


def test_handle_command_birthdays_via_dispatch(empty_address_book):
    """
    Given a contact with an upcoming birthday on a frozen date (2026-05-19)
    When birthdays is dispatched via handle_command
    Then the output contains the formatted upcoming birthday line
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
    """
    Given an address book and parametrized commands with wrong argument counts
    When handle_command is dispatched
    Then the invalid-command message is returned
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
    """
    Given an empty or whitespace command string
    When handle_command is dispatched
    Then the invalid-command message is returned
    """
    assert handle_command(empty_address_book, command, arguments) == expected


def test_handle_command_phone_no_user(empty_address_book):
    """
    Given an empty address book
    When phone is dispatched for a missing user
    Then the no-such-user message is returned
    """
    assert (
        handle_command(empty_address_book, "phone", ["Ghost"])
        == COMMAND_MESSAGES["NO_SUCH_USER"]
    )


def test_handle_command_update_no_user(empty_address_book, valid_phone):
    """
    Given an empty address book
    When update is dispatched for a missing user
    Then the no-such-user message is returned
    """
    assert (
        handle_command(empty_address_book, "update", ["Ghost", valid_phone])
        == COMMAND_MESSAGES["NO_SUCH_USER"]
    )


def test_handle_command_exit_close_returns_none(empty_address_book):
    """
    Given an address book
    When exit or close is dispatched
    Then the goodbye message is returned and the book is unchanged
    """
    assert (
        handle_command(empty_address_book, "exit", []) == COMMAND_MESSAGES["GOOD_BYE"]
    )
    assert (
        handle_command(empty_address_book, "close", []) == COMMAND_MESSAGES["GOOD_BYE"]
    )
    assert len(empty_address_book.data) == 0
