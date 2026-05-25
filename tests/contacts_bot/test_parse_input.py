import pytest

from src.scripts.contacts_bot import parse_input
from tests.contacts_bot.shared import INVALID_PHONE_12, INVALID_PHONE_15


@pytest.mark.parametrize(
    "line,expected_cmd,expected_args",
    [
        ("hello", "hello", []),
        ("HELLO", "hello", []),
        ("Hello", "hello", []),
        ("  hello  ", "hello", []),
        (f"add Alice {INVALID_PHONE_12}", "add", ["Alice", INVALID_PHONE_12]),
        (f"aDd Bob {INVALID_PHONE_15}", "add", ["Bob", INVALID_PHONE_15]),
        (f"upDaTe carol {INVALID_PHONE_12}", "update", ["carol", INVALID_PHONE_12]),
        (f"UpDaTe dave {INVALID_PHONE_12}", "update", ["dave", INVALID_PHONE_12]),
        (
            "add-birthday JohnDoe 01.01.1990",
            "add-birthday",
            ["JohnDoe", "01.01.1990"],
        ),
        ("show-birthday JohnDoe", "show-birthday", ["JohnDoe"]),
        ("birthdays", "birthdays", []),
        ("Phone Eve", "phone", ["Eve"]),
        ("PhOnE Frank", "phone", ["Frank"]),
        ("all", "all", []),
        ("ALL", "all", []),
        ("exIt", "exit", []),
        ("cLose", "close", []),
    ],
)
def test_parse_input_tokenization(line, expected_cmd, expected_args):
    """
    Given a parametrized command line (mixed case and spacing)
    When parse_input is called
    Then the command is lowercased and arguments are split as expected
    """
    cmd, args = parse_input(line)
    assert cmd == expected_cmd
    assert args == expected_args


@pytest.mark.parametrize(
    "line,expected_cmd,expected_args",
    [
        ("", "", []),
        ("   \t  ", "", []),
    ],
)
def test_parse_input_empty_and_blank(line, expected_cmd, expected_args):
    """
    Given an empty or whitespace-only line
    When parse_input is called
    Then the command is empty and arguments are an empty list
    """
    cmd, args = parse_input(line)
    assert cmd == expected_cmd
    assert args == expected_args
