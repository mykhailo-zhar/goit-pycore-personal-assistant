from src.decorators.input_error import input_error
from src.note_book import NoteBook

INSERT_TEXT_MESSAGES = {
    "INVALID_SYNTAX": "Insert text command should have the following syntax: insert-text <title> <text*>",
    "NO_TEXT": "No text",
    "NO_SUCH_NOTE": "No such note",
    "TEXT_INSERTED": "Text inserted",
}


@input_error
def insert_text(note_book: NoteBook, arguments: list[str]) -> str:
    """
    Додає або замінює текст нотатки.

    Аргументи:
        note_book (NoteBook): Книга нотаток.
        arguments (list[str]): Заголовок і текст.
    """

    match len(arguments):
        case 0:
            raise ValueError(INSERT_TEXT_MESSAGES["INVALID_SYNTAX"])
        case 1:
            raise ValueError(INSERT_TEXT_MESSAGES["NO_TEXT"])
        case _:
            pass

    title = arguments[0]
    text = " ".join(arguments[1:])

    note = note_book.find_note(title)
    if note is None:
        raise KeyError(INSERT_TEXT_MESSAGES["NO_SUCH_NOTE"])

    note.text = text
    return INSERT_TEXT_MESSAGES["TEXT_INSERTED"]
