import pytest

from src.scripts.contacts_bot import COMMAND_MESSAGES, add_contact, show_phone


@pytest.mark.parametrize(
    "arguments,expected",
    [
        (["JohnDoe"], "1234567890"),
        (["Bob"], COMMAND_MESSAGES["NO_SUCH_USER"]),
        (["no@pe"], COMMAND_MESSAGES["NO_SUCH_USER"]),
        (["JohnDoe", "123456789012"], COMMAND_MESSAGES["INVALID_COMMAND"]),
    ],
)
def test_show_phone(empty_address_book, arguments, expected):
    add_contact(empty_address_book, ["JohnDoe", "1234567890"])
    assert show_phone(empty_address_book, arguments) == expected


def test_show_phone_multiple_phones(empty_address_book, valid_phone_generator):
    valid_phones = [valid_phone_generator() for _ in range(3)]
    for phone in valid_phones:
        add_contact(empty_address_book, ["JohnDoe", phone])
    assert show_phone(empty_address_book, ["JohnDoe"]) == "; ".join(valid_phones)
