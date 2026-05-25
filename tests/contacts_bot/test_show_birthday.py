import pytest

from src.scripts.contacts_bot import COMMAND_MESSAGES, add_birthday, show_birthday


def test_show_birthday_returns_existing_birthday(book_with_contact, valid_birthday_str):
    add_birthday(book_with_contact, ["JohnDoe", valid_birthday_str])

    assert show_birthday(book_with_contact, ["JohnDoe"]) == COMMAND_MESSAGES[
        "BIRTHDAY_SHOWED"
    ].format(name="JohnDoe", birthday=valid_birthday_str)


def test_show_birthday_reads_record_stored_in_address_book(
    book_with_contact, valid_birthday_str
):
    record = book_with_contact.data["JohnDoe"]
    record.add_birthday(valid_birthday_str)

    assert show_birthday(book_with_contact, ["JohnDoe"]) == COMMAND_MESSAGES[
        "BIRTHDAY_SHOWED"
    ].format(name="JohnDoe", birthday=valid_birthday_str)


def test_show_birthday_no_such_user(empty_address_book):
    assert (
        show_birthday(empty_address_book, ["Nobody"])
        == COMMAND_MESSAGES["NO_SUCH_USER"]
    )


def test_show_birthday_no_birthday(book_with_contact):
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
    assert (
        show_birthday(book_with_contact, arguments)
        == COMMAND_MESSAGES["INVALID_COMMAND"]
    )
