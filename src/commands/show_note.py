from src.decorators.input_error import input_error
from src.note_book import NoteBook
from src.presenters.note import NotePresenter

SHOW_NOTE_MESSAGES = {
    "INVALID_SYNTAX": "Note command should have the following syntax: note <title>",
    "NO_SUCH_NOTE": "No such note",
    "TITLE_LABEL": "Note title: ",
    "TEXT_LABEL": "text: ",
    "TAGS_LABEL": "tags: ",
}


@input_error
def show_note(note_book: NoteBook, arguments: list[str]) -> str:
    """
    Показує інформацію про нотатку.

    Аргументи:
        note_book (NoteBook): Книга нотаток.
        arguments (list[str]): Заголовок нотатки.
    """
    if len(arguments) != 1:
        raise ValueError(SHOW_NOTE_MESSAGES["INVALID_SYNTAX"])

    title = arguments[0]
    note = note_book.find_note(title)
    if note is None:
        raise KeyError(SHOW_NOTE_MESSAGES["NO_SUCH_NOTE"])

    return str(NotePresenter(note))
