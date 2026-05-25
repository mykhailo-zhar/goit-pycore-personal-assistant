import pytest

from src.fields.birthday import Birthday
from src.fields.field import Field


def test_birthday_is_subclass_of_field():
    """
    Given the Birthday and Field classes
    When checking the class hierarchy
    Then Birthday is a subclass of Field
    """
    assert issubclass(Birthday, Field)


@pytest.fixture
def valid_birthday_str():
    return "10.01.1990"


@pytest.fixture
def valid_birthday(valid_birthday_str):
    return Birthday(valid_birthday_str)


def test_birthday_init(valid_birthday, valid_birthday_str):
    """
    Given a Birthday constructed with a valid DD.MM.YYYY string
    When the value attribute is read
    Then it equals the input string
    """
    assert valid_birthday.value == valid_birthday_str


def test_birthday_str(valid_birthday, valid_birthday_str):
    """
    Given a Birthday with a valid date string
    When str() is called on the birthday
    Then the result equals the stored value
    """
    assert str(valid_birthday) == valid_birthday_str


def test_birthday_validate(valid_birthday):
    """
    Given a Birthday with value "10.01.1990"
    When validate() is called
    Then it returns True
    """
    assert valid_birthday.validate()


@pytest.mark.parametrize(
    "birthday",
    [
        ("1990-01-01"),
        ("10/01/1990"),
        ("10.13.1990"),
        ("test"),
        (None),
        (10),
        (10.0),
        (True),
        (False),
        (["10.01.1990"]),
        ({"10.01.1990": "10.01.1990"}),
        ({"10.01.1990"}),
    ],
)
def test_birthday_validate_invalid(birthday):
    """
    Given a parametrized invalid birthday value
    When Birthday(birthday).validate() is called
    Then it returns False
    """
    assert not Birthday(birthday).validate()
