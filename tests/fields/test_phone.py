import pytest

from src.fields.field import Field
from src.fields.phone import Phone


def test_phone_is_subclass_of_field():
    assert issubclass(Phone, Field)


@pytest.fixture
def valid_phone():
    return Phone("1234567890")


def test_phone_init(valid_phone):
    assert valid_phone.value == "1234567890"


def test_phone_str(valid_phone):
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
    phone = Phone(phone)
    assert phone.validate() == is_valid
