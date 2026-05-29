import pytest

from src.fields.field import Field
from src.fields.title import Title
from tests.fields.conftest import random_text


def test_title_is_subclass_of_field():
    assert issubclass(Title, Field)


@pytest.fixture
def title(request):
    if isinstance(request.param, int):
        return random_text(request.param)
    elif isinstance(request.param, list):
        return "-".join(request.param)
    else:
        return request.param


@pytest.mark.parametrize(
    "title",
    [
        "test",
        "test123",
        1,
        30,
        100,
        ["test", "test"],
    ],
    indirect=True,
)
def test_title_is_valid(title):
    assert Title(title).validate()


@pytest.mark.parametrize(
    "title",
    ["", 101],
    indirect=True,
)
def test_title_is_invalid(title):
    assert not Title(title).validate()
