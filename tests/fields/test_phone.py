import pytest

from src.fields.field import Field
from src.fields.phone import Phone


def test_phone_is_subclass_of_field():
    """
    Given the Phone and Field classes
    When checking the class hierarchy
    Then Phone is a subclass of Field
    """
    assert issubclass(Phone, Field)


@pytest.fixture
def valid_phone():
    return Phone("1234567890")


def test_phone_init(valid_phone):
    """
    Given a Phone constructed with "1234567890"
    When the value attribute is read
    Then it equals "1234567890"
    """
    assert valid_phone.value == "1234567890"


def test_phone_str(valid_phone):
    """
    Given a Phone with value "1234567890"
    When str() is called on the phone
    Then the result is "1234567890"
    """
    assert str(valid_phone) == "1234567890"


@pytest.mark.parametrize(
    "phone, is_valid",
    [
        ("1234567", False),
        ("1234567890", True),
        ("12345678901", False),
        ("123456789012", False),
        ("123456789a", False),
    ],
)
def test_phone_validate(phone, is_valid):
    """
    Given a parametrized phone string
    When Phone(phone).validate() is called
    Then the result matches the expected validity for that case
    """
    phone = Phone(phone)
    assert phone.validate() == is_valid
