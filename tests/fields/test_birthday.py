import pytest

from src.fields.birthday import Birthday
from src.fields.field import Field


def test_birthday_is_subclass_of_field():
    assert issubclass(Birthday, Field)


@pytest.fixture
def valid_birthday_str():
    return "10.01.1990"


@pytest.fixture
def valid_birthday(valid_birthday_str):
    return Birthday(valid_birthday_str)


def test_birthday_init(valid_birthday, valid_birthday_str):
    assert valid_birthday.value == valid_birthday_str


def test_birthday_str(valid_birthday, valid_birthday_str):
    assert str(valid_birthday) == valid_birthday_str


def test_birthday_validate(valid_birthday):
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
    assert not Birthday(birthday).validate()
