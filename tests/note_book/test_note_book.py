import pytest

from src.note import Note
from src.note_book import NoteBook


@pytest.fixture
def valid_title():
    return "my-note"


@pytest.fixture
def note(valid_title):
    return Note(valid_title)


@pytest.fixture
def note_book():
    return NoteBook()


def test_note_book_init(note_book):
    """Перевіряє початковий стан нової книги нотаток.

    Дано:
        Нова ``NoteBook``.
    Коли:
        Зчитується атрибут ``data``.
    Тоді:
        Це порожній словник.
    """
    assert note_book.data == {}


def test_note_book_add_note(note_book, note, valid_title):
    """Перевіряє додавання нотатки до книги.

    Дано:
        Порожня ``NoteBook`` і ``Note``.
    Коли:
        Викликається ``add_note``.
    Тоді:
        Нотатка зберігається за ключем заголовка.

    Args:
        note_book: Порожня книга нотаток.
        note: Нотатка для додавання.
        valid_title: Заголовок нотатки.
    """
    note_book.add_note(note)
    assert note_book.data == {valid_title: note}


def test_note_book_add_duplicate_note_raises_key_error(note_book, note, valid_title):
    """Перевіряє заборону дублювання заголовка при додаванні.

    Дано:
        ``NoteBook`` із нотаткою з таким заголовком.
    Коли:
        Додається інша нотатка з тим самим заголовком.
    Тоді:
        Виникає ``KeyError``.

    Args:
        note_book: Книга з однією нотаткою.
        note: Існуюча нотатка.
        valid_title: Заголовок, що вже зайнятий.
    """
    note_book.add_note(note)
    with pytest.raises(KeyError):
        note_book.add_note(Note(valid_title))


def test_note_book_find_note(note_book, note, valid_title):
    """Перевіряє пошук наявної нотатки.

    Дано:
        ``NoteBook`` із доданою нотаткою.
    Коли:
        Викликається ``find_note`` із заголовком нотатки.
    Тоді:
        Повертається той самий екземпляр ``Note``.

    Args:
        note_book: Книга з однією нотаткою.
        note: Очікувана нотатка.
        valid_title: Заголовок нотатки.
    """
    note_book.add_note(note)
    assert note_book.find_note(valid_title) == note


def test_note_book_find_non_existent_note(note_book, valid_title):
    """Перевіряє пошук відсутньої нотатки.

    Дано:
        Порожня ``NoteBook``.
    Коли:
        Викликається ``find_note`` для неіснуючого заголовка.
    Тоді:
        Повертається ``None``.

    Args:
        note_book: Порожня книга нотаток.
        valid_title: Заголовок, якого немає в книзі.
    """
    assert note_book.find_note(valid_title) is None


def test_note_book_change_title(note_book, note, valid_title):
    """Перевіряє зміну заголовка нотатки.

    Дано:
        ``NoteBook`` із нотаткою.
    Коли:
        Викликається ``change_title`` з новим валідним заголовком.
    Тоді:
        Нотатка знаходиться за новим заголовком, старий ключ зникає.

    Args:
        note_book: Книга з однією нотаткою.
        note: Нотатка для перейменування.
        valid_title: Початковий заголовок.
    """
    new_title = "renamed-note"
    note_book.add_note(note)
    note_book.change_title(valid_title, new_title)
    assert note_book.find_note(valid_title) is None
    assert note_book.find_note(new_title) == note
    assert note.title.value == new_title


def test_note_book_change_title_not_found_raises_key_error(note_book):
    """Перевіряє ``KeyError``, якщо нотатку для перейменування не знайдено.

    Дано:
        Порожня ``NoteBook``.
    Коли:
        Викликається ``change_title`` для неіснуючого заголовка.
    Тоді:
        Виникає ``KeyError``.

    Args:
        note_book: Порожня книга нотаток.
    """
    with pytest.raises(KeyError):
        note_book.change_title("missing", "new-title")


def test_note_book_change_title_collision_raises_key_error(note_book, note, valid_title):
    """Перевіряє ``KeyError`` при колізії нового заголовка.

    Дано:
        ``NoteBook`` із двома нотатками.
    Коли:
        ``change_title`` намагається перейменувати в зайнятий заголовок.
    Тоді:
        Виникає ``KeyError``.

    Args:
        note_book: Книга з двома нотатками.
        note: Нотатка для перейменування.
        valid_title: Початковий заголовок першої нотатки.
    """
    other_title = "other-note"
    note_book.add_note(note)
    note_book.add_note(Note(other_title))
    with pytest.raises(KeyError):
        note_book.change_title(valid_title, other_title)


def test_note_book_remove_note(note_book, note, valid_title):
    """Перевіряє видалення наявної нотатки.

    Дано:
        ``NoteBook`` із нотаткою.
    Коли:
        Викликається ``remove_note`` із заголовком нотатки.
    Тоді:
        Повертається ``True`` і нотатка більше не знаходиться.

    Args:
        note_book: Книга з однією нотаткою.
        note: Нотатка для видалення.
        valid_title: Заголовок нотатки.
    """
    note_book.add_note(note)
    assert note_book.remove_note(valid_title)
    assert note_book.find_note(valid_title) is None


def test_note_book_remove_non_existent_note(note_book, valid_title):
    """Перевіряє видалення відсутньої нотатки.

    Дано:
        Порожня ``NoteBook``.
    Коли:
        Викликається ``remove_note`` для неіснуючого заголовка.
    Тоді:
        Повертається ``False``.

    Args:
        note_book: Порожня книга нотаток.
        valid_title: Заголовок, якого немає в книзі.
    """
    assert not note_book.remove_note(valid_title)
