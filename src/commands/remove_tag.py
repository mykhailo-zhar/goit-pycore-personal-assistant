from src.decorators.input_error import input_error
from src.note_book import NoteBook

REMOVE_TAG_MESSAGES = {
    "INVALID_SYNTAX": "Remove tag command should have the following syntax: remove-tag <title> <tag>",
    "NO_SUCH_NOTE": "There is no such note",
    "NO_TAG_ON_NOTE": "There is no tag on the note",
    "TAG_REMOVED": "Tag removed",
}


@input_error
def remove_tag(note_book: NoteBook, arguments: list[str]) -> str:
    """
    Видаляє тег з нотатки.

    Аргументи:
        note_book (NoteBook): Книга нотаток.
        arguments (list[str]): Заголовок і тег.
    """
    if len(arguments) != 2:
        raise ValueError(REMOVE_TAG_MESSAGES["INVALID_SYNTAX"])

    title, tag = arguments
    note = note_book.find_note(title)
    if note is None:
        raise KeyError(REMOVE_TAG_MESSAGES["NO_SUCH_NOTE"])

    if note.find_tag(tag) is None:
        raise ValueError(REMOVE_TAG_MESSAGES["NO_TAG_ON_NOTE"])

    note.remove_tag(tag)
    return REMOVE_TAG_MESSAGES["TAG_REMOVED"]
