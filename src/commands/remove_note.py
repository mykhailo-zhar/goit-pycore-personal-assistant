from src.note import Note
from src.note_book import NoteBook
from src.utils.decorators.input_error import input_error

REMOVE_NOTE_MESSAGES = {
    "INVALID_SYNTAX": "Remove note command should have the following syntax: remove-note <title>",
    "NOTE_ALREADY_DELETED": "Note is already deleted.",
    "NOTE_NOT_FOUND": "Note not found.",
}


@input_error
def remove_note(note_book: NoteBook, arguments: list[str]) -> str:
    """
    Видаляє нотатку за заголовком.

    Аргументи:
        title (str): Заголовок нотатки для видалення.

    Повертає:
        bool: True, якщо нотатку знайдено і видалено, інакше False.
    """
    if len(arguments) != 1:
        raise ValueError(REMOVE_NOTE_MESSAGES["INVALID_SYNTAX"])
    title = arguments[0]

    is_removed = note_book.remove_note(title)

    if is_removed:
        return REMOVE_NOTE_MESSAGES["NOTE_ALREADY_DELETED"]

    return REMOVE_NOTE_MESSAGES["NOTE_NOT_FOUND"]
