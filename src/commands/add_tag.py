from src.note_book import NoteBook
from src.utils.decorators.input_error import input_error

ADD_TAG_MESSAGES = {
    "INVALID_SYNTAX": "Add tag command should have the following syntax: add-tag <title> <tag>",
    "NO_SUCH_NOTE": "There is no such note",
    "TAG_ALREADY_EXISTS": "There is already such tag",
    "TAG_ADDED": "Tag added",
}


@input_error
def add_tag(note_book: NoteBook, arguments: list[str]) -> str:
    """
    Додає тег до нотатки.

    Аргументи:
        note_book (NoteBook): Книга нотаток.
        arguments (list[str]): Заголовок і тег.
    """
    if len(arguments) != 2:
        raise ValueError(ADD_TAG_MESSAGES["INVALID_SYNTAX"])

    title, tag = arguments
    note = note_book.find_note(title)
    if note is None:
        raise KeyError(ADD_TAG_MESSAGES["NO_SUCH_NOTE"])

    if note.find_tag(tag) is not None:
        raise ValueError(ADD_TAG_MESSAGES["TAG_ALREADY_EXISTS"])

    note.add_tag(tag)
    return ADD_TAG_MESSAGES["TAG_ADDED"]
