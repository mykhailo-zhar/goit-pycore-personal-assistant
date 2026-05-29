from pathlib import Path

import pytest

from src.note import Note
from tests.fields.conftest import random_text

CONTACTS_BOT_PATH = Path(__file__).parent.parent / "src" / "scripts" / "contacts_bot.py"


@pytest.fixture
def valid_title():
    return "my-note"


@pytest.fixture
def note(valid_title):
    return Note(valid_title)


def test_note_init(valid_title):
    """Перевіряє збереження заголовка при створенні нотатки.

    Дано:
        Валідний заголовок.
    Коли:
        Створюється ``Note``.
    Тоді:
        Заголовок зберігається в нотатці.

    Args:
        valid_title: Валідний заголовок нотатки.
    """
    note = Note(valid_title)
    assert note.title.value == valid_title


@pytest.mark.parametrize("invalid_title", ["", random_text(101)])
def test_note_init_invalid_title_raises_value_error(invalid_title):
    """Перевіряє відхилення невалідного заголовка при створенні.

    Дано:
        Порожній заголовок або довший за 100 символів.
    Коли:
        Створюється ``Note``.
    Тоді:
        Виникає ``ValueError``.

    Args:
        invalid_title: Невалідний заголовок.
    """
    with pytest.raises(ValueError):
        Note(invalid_title)


def test_note_edit_title(note):
    """Перевіряє зміну заголовка через ``edit_title``.

    Дано:
        Нотатка з валідним заголовком.
    Коли:
        Викликається ``edit_title`` з новим валідним заголовком.
    Тоді:
        Заголовок оновлюється.

    Args:
        note: Нотатка з початковим заголовком.
    """
    new_title = "renamed-note"
    note.edit_title(new_title)
    assert note.title.value == new_title


def test_note_edit_title_invalid_raises_value_error(note):
    """Перевіряє відхилення невалідного заголовка при ``edit_title``.

    Дано:
        Нотатка з валідним заголовком.
    Коли:
        ``edit_title`` викликається з заголовком довшим за 100 символів.
    Тоді:
        Виникає ``ValueError``.

    Args:
        note: Нотатка з валідним заголовком.
    """
    with pytest.raises(ValueError):
        note.edit_title(random_text(101))


def test_note_add_tag(note):
    """Перевіряє додавання валідного тегу.

    Дано:
        Нотатка без тегів.
    Коли:
        Викликається ``add_tag`` з валідним тегом.
    Тоді:
        Тег відображається в ``show_tags``.

    Args:
        note: Нотатка без тегів.
    """
    note.add_tag("work")
    assert note.show_tags() == "work"


def test_note_add_tag_invalid_raises_value_error(note):
    """Перевіряє відхилення невалідного тегу.

    Дано:
        Нотатка без тегів.
    Коли:
        Додається тег із недопустимими символами.
    Тоді:
        Виникає ``ValueError``.

    Args:
        note: Нотатка без тегів.
    """
    with pytest.raises(ValueError):
        note.add_tag("invalid_tag")


def test_note_add_duplicate_tag_raises_value_error(note):
    """Перевіряє заборону дублювання тегу.

    Дано:
        Нотатка з уже доданим тегом.
    Коли:
        Той самий тег додається знову.
    Тоді:
        Виникає ``ValueError``.

    Args:
        note: Нотатка з одним тегом.
    """
    note.add_tag("work")
    with pytest.raises(ValueError):
        note.add_tag("work")


def test_note_show_tags_empty(note):
    """Перевіряє порожній рядок за відсутності тегів.

    Дано:
        Нотатка без тегів.
    Коли:
        Викликається ``show_tags``.
    Тоді:
        Повертається порожній рядок.

    Args:
        note: Нотатка без тегів.
    """
    assert note.show_tags() == ""


def test_note_show_tags_multiple(note):
    """Перевіряє відображення кількох тегів.

    Дано:
        Нотатка з кількома тегами.
    Коли:
        Викликається ``show_tags``.
    Тоді:
        Повертається рядок із усіма тегами через кому.

    Args:
        note: Нотатка без тегів.
    """
    note.add_tag("work")
    note.add_tag("urgent")
    tags = note.show_tags()
    assert all(tag in tags for tag in ["work", "urgent"])


def test_note_remove_tag(note):
    """Перевіряє успішне видалення існуючого тегу.

    Дано:
        Нотатка з доданим тегом.
    Коли:
        Викликається ``remove_tag`` для цього тегу.
    Тоді:
        Повертається ``True`` і тег більше не відображається.

    Args:
        note: Нотатка з тегом.
    """
    note.add_tag("work")
    assert note.remove_tag("work")
    assert "work" not in note._tags


def test_note_remove_non_existent_tag(note):
    """Перевіряє видалення відсутнього тегу.

    Дано:
        Нотатка без тегів.
    Коли:
        Викликається ``remove_tag`` для неіснуючого тегу.
    Тоді:
        Повертається ``False``.

    Args:
        note: Нотатка без тегів.
    """
    assert not note.remove_tag("missing")
