from src.decorators.input_error import input_error
from src.note_book import NoteBook

CHANGE_TITLE_MESSAGES = {
    "INVALID_SYNTAX": "Change title command should have the following syntax: change-title <old_title> <new_title>",
    "NO_SUCH_NOTE": "No such note",
    "NOTE_ALREADY_EXISTS": "Note already exists",
    "TITLE_CHANGED": "Title was changed",
}


@input_error
def change_title(note_book: NoteBook, arguments: list[str]) -> str:
    """
    Змінює заголовок нотатки.

    Аргументи:
        note_book (NoteBook): Книга нотаток.
        arguments (list[str]): Старий і новий заголовки.
    """
    if len(arguments) != 2:
        raise ValueError(CHANGE_TITLE_MESSAGES["INVALID_SYNTAX"])

    old_title, new_title = arguments
    note = note_book.find_note(old_title)
    if note is None:
        raise ValueError(CHANGE_TITLE_MESSAGES["NO_SUCH_NOTE"])

    if old_title != new_title and note_book.find_note(new_title) is not None:
        raise KeyError(CHANGE_TITLE_MESSAGES["NOTE_ALREADY_EXISTS"])

    note_book.change_title(old_title, new_title)
    return CHANGE_TITLE_MESSAGES["TITLE_CHANGED"]
