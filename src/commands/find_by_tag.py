from enum import Enum

from src.decorators.input_error import input_error
from src.note_book import NoteBook
from src.presenters.note import NotePresenter

FIND_BY_TAG_MESSAGES = {
    "INVALID_SYNTAX": "Tag command should have the following syntax: tag <tag> <order>",
    "INVALID_ORDER": "There are only ascending and descending order.",
    "NO_NOTES": "There are no notes,",
}


class ValidOrders(Enum):
    ASCENDING = "ascending"
    DESCENDING = "descending"


@input_error
def find_by_tag(note_book: NoteBook, arguments: list[str]) -> str:
    """
    Показує нотатки з вказаним тегом, відсортовані за заголовком.

    Аргументи:
        note_book (NoteBook): Книга нотаток.
        arguments (list[str]): Тег і порядок сортування.
    """
    if len(arguments) != 2:
        raise ValueError(FIND_BY_TAG_MESSAGES["INVALID_SYNTAX"])

    tag, order = arguments
    if order not in ValidOrders:
        raise ValueError(FIND_BY_TAG_MESSAGES["INVALID_ORDER"])

    matched = [
        note for note in note_book.data.values() if note.find_tag(tag) is not None
    ]
    if not matched:
        raise ValueError(FIND_BY_TAG_MESSAGES["NO_NOTES"])

    matched.sort(
        key=lambda note: note.title.value, reverse=order == ValidOrders.DESCENDING.value
    )
    return str(NotePresenter(matched))
