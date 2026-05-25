import pytest

from src.scripts.contacts_bot import COMMAND_MESSAGES, add_birthday

from .shared import RECORD_ERRORS


def test_add_birthday_adds_to_existing_record(book_with_contact, valid_birthday_str):
    """
    Given a contact without a birthday
    When add_birthday is called with a valid date
    Then the birthday-added message is returned and the date is stored
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
    """
    Given a reference to the contact record in the book
    When add_birthday is called
    Then the same record object in the book is updated with the birthday
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
    """
    Given an empty address book
    When add_birthday is called for a missing user
    Then the no-such-user message is returned and the book stays empty
    """
    assert (
        add_birthday(empty_address_book, ["Nobody", valid_birthday_str])
        == COMMAND_MESSAGES["NO_SUCH_USER"]
    )
    assert len(empty_address_book.data) == 0


def test_add_birthday_invalid_birthday(book_with_contact, invalid_birthday_str):
    """
    Given a contact without a birthday
    When add_birthday is called with an invalid date
    Then a validation error is returned and birthday remains unset
    """
    assert add_birthday(
        book_with_contact, ["JohnDoe", invalid_birthday_str]
    ) == RECORD_ERRORS["BIRTHDAY_NOT_VALID"].format(birthday=invalid_birthday_str)
    assert book_with_contact.data["JohnDoe"].birthday is None


def test_add_birthday_replaces_existing_birthday(
    book_with_contact, valid_birthday_str, new_valid_birthday_str
):
    """
    Given a contact that already has a birthday
    When add_birthday is called with a new valid date
    Then the message shows old and new dates and the birthday is replaced
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
    """
    Given a contact in the book and parametrized wrong argument counts
    When add_birthday is called
    Then the invalid-command message is returned
    """
    assert (
        add_birthday(book_with_contact, arguments)
        == COMMAND_MESSAGES["INVALID_COMMAND"]
    )
