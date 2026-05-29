from src.note_book import NoteBook
from src.utils.decorators.input_error import input_error
from src.messages import INSERT_TEXT_MESSAGES


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
