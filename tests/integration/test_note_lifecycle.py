import builtins

from main import main
from src.serializers.note_book import NoteBookSerializer


def test_note_lifecycle(monkeypatch, capsys, tmp_path):
    """Перевіряє повний цикл створення, редагування та показу нотатки.

    Дано:
        Порожня книга нотаток.
    Коли:
        Послідовно виконуються команди ``add-note``, ``insert-text``,
        ``change-title`` та ``note``.
    Тоді:
        Нотатка зберігається під новим заголовком із текстом,
        у виводі з'являється її рядкове подання.
    """
    note_serializer = NoteBookSerializer(str(tmp_path / "notebook.pkl"))
    lines = iter(
        [
            "add-note work",
            "insert-text work First line of notes",
            "change-title work personal",
            "note personal",
            "exit",
        ]
    )
    monkeypatch.setattr(builtins, "input", lambda: next(lines))
    monkeypatch.setattr(
        "main.NOTE_SERIALIZER_PATH",
        note_serializer.file_path,
    )
    main()

    note_book = note_serializer.deserialize()
    note = note_book.find_note("personal")
    assert note is not None
    assert note.text.value == "First line of notes"
    assert note_book.find_note("work") is None

    out = capsys.readouterr().out
    assert note.title.value in out
    assert note.text.value in out
    assert note.show_tags() in out
