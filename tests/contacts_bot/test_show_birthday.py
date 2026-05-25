import pytest

from src.scripts.contacts_bot import COMMAND_MESSAGES, add_birthday, show_birthday


def test_show_birthday_returns_existing_birthday(book_with_contact, valid_birthday_str):
    """
    Given a contact with a birthday set via add_birthday
    When show_birthday is called
    Then the formatted birthday message for that contact is returned
    """
    add_birthday(book_with_contact, ["JohnDoe", valid_birthday_str])

    assert show_birthday(book_with_contact, ["JohnDoe"]) == COMMAND_MESSAGES[
        "BIRTHDAY_SHOWED"
    ].format(name="JohnDoe", birthday=valid_birthday_str)


def test_show_birthday_reads_record_stored_in_address_book(
    book_with_contact, valid_birthday_str
):
    """
    Given a birthday set directly on the record in the book
    When show_birthday is called
    Then the formatted birthday message is returned
    """
    record = book_with_contact.data["JohnDoe"]
    record.add_birthday(valid_birthday_str)

    assert show_birthday(book_with_contact, ["JohnDoe"]) == COMMAND_MESSAGES[
        "BIRTHDAY_SHOWED"
    ].format(name="JohnDoe", birthday=valid_birthday_str)


def test_show_birthday_no_such_user(empty_address_book):
    """
    Given an empty address book
    When show_birthday is called for a missing user
    Then the no-such-user message is returned
    """
    assert (
        show_birthday(empty_address_book, ["Nobody"])
        == COMMAND_MESSAGES["NO_SUCH_USER"]
    )


def test_show_birthday_no_birthday(book_with_contact):
    """
    Given a contact without a birthday
    When show_birthday is called
    Then the no-birthday-set message is returned
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
    """
    Given a contact in the book and parametrized wrong argument counts
    When show_birthday is called
    Then the invalid-command message is returned
    """
    assert (
        show_birthday(book_with_contact, arguments)
        == COMMAND_MESSAGES["INVALID_COMMAND"]
    )
