import pytest

from src.fields.field import Field
from src.fields.name import Name


def test_name_is_subclass_of_field():
    assert issubclass(Name, Field)


def test_name_init():
    name = Name("John Doe")
    assert name.value == "John Doe"


def test_name_str():
    name = Name("John Doe")
    assert str(name) == "John Doe"


@pytest.mark.parametrize(
    "name, is_valid",
    [
        (10, False),
        ("", False),
        (None, False),
        ("John Doe", False),
        ("John Doe1", False),
        ("JohnDoe1", True),
        ("John", True),
    ],
)
def test_name_validate(name, is_valid):
    assert Name(name).validate() == is_valid
