from src.note import Note
from src.note_book import NoteBook
from src.utils.decorators.input_error import input_error
from src.messages import ADD_NOTE_MESSAGES


@input_error
def add_note(note_book: NoteBook, arguments: list[str]) -> str:
    """
    Додає порожню нотатку.

    Аргументи:
        note_book (NoteBook): Книга нотаток.
        arguments (list[str]): Заголовок нотатки.
    """
    if len(arguments) != 1:
        raise ValueError(ADD_NOTE_MESSAGES["INVALID_SYNTAX"])

    title = arguments[0]
    if note_book.find_note(title):
        raise KeyError(ADD_NOTE_MESSAGES["NOTE_ALREADY_PRESENT"])

    note_book.add_note(Note(title))
    return ADD_NOTE_MESSAGES["NOTE_ADDED"].format(title=title)
