from collections.abc import Callable
from typing import assert_type

import pytest

from src.fields.field import Field


@pytest.fixture
def field():
    return Field("test")


def test_field_init(field):
    assert field.value == "test"


def test_field_str(field):
    assert str(field) == "test"


def test_field_has_validate(field):
    assert assert_type(field.validate, Callable[[], bool])
