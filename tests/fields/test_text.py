import pytest

from src.fields.field import Field
from src.fields.text import Text


def test_text_is_subclass_of_field():
    assert issubclass(Text, Field)


@pytest.mark.parametrize(
    "text",
    ["test", "test123", "1213123@172314124#@##$$#"],
)
def test_text_is_valid(text):
    assert Text(text).validate()


@pytest.mark.parametrize(
    "text",
    [1, "", "       ", None, [], {}, ()],
)
def test_text_is_invalid(text):
    assert not Text(text).validate()
