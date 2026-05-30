from src.fields.address import Address
from src.fields.field import Field
import pytest


def test_address_is_subclass_of_field():
    assert issubclass(Address, Field)


@pytest.mark.parametrize(
    "address",
    [
        ("123 Main St"),
        ("123 Main St, Apt 1"),
        ("123 Main St, Apt 1, City, State, 12345"),
        ("123 Main St, Apt 1, City, State, 12345-6789"),
        ("123 Main St, Apt 1, City, State, 12345-6789, USA"),
        ("123 Main St, Apt 1, City, State, 12345-6789, USA"),
    ],
)
def test_address_valid(address):
    assert Address(address).validate()


def test_address_invalid():
    assert not Address("").validate()
