import pytest

from src.fields.field import Field
from src.fields.name import Name


def test_name_is_subclass_of_field():
    """
    Given the Name and Field classes
    When checking the class hierarchy
    Then Name is a subclass of Field
    """
    assert issubclass(Name, Field)


def test_name_init():
    """
    Given the string "John Doe"
    When a Name instance is created
    Then its value equals "John Doe"
    """
    name = Name("John Doe")
    assert name.value == "John Doe"


def test_name_str():
    """
    Given a Name with value "John Doe"
    When str() is called on the name
    Then the result is "John Doe"
    """
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
    """
    Given a parametrized candidate name value
    When Name(name).validate() is called
    Then the result matches the expected validity for that case
    """
    assert Name(name).validate() == is_valid
