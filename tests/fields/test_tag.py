from src.fields.tag import Tag
from src.fields.field import Field
from tests.fields.conftest import random_text
import pytest

def test_tag_is_subclass_of_field():
    assert issubclass(Tag, Field)

@pytest.fixture
def tag(request):
  if isinstance(request.param, int):
    return random_text(request.param)
  elif isinstance(request.param, list):
    return  " ".join(request.param)
  else: 
    return request.param

@pytest.mark.parametrize(
    "tag",
    [
        "test",
        "test123",
        1,
        30,
    ],
    indirect=True,
)
def test_tag_is_valid(tag):
    assert Tag(tag).validate()

@pytest.mark.parametrize(
    "tag",
    [
        "",
        "test123_test123",
        31,
        ["test", "test"]
    ],
    indirect=True,
)
def test_tag_is_invalid(tag):
    assert not Tag(tag).validate()