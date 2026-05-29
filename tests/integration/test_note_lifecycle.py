import builtins

from src.scripts.contacts_bot import main
from src.utils.serializers.note_book import NoteBookSerializer


def test_note_lifecycle(monkeypatch, capsys, tmp_path):
    """Перевіряє повний цикл створення, редагування та показу нотатки."""
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
        "src.scripts.contacts_bot.NOTE_SERIALIZER_PATH",
        note_serializer.file_path,
    )
    main()

    note_book = note_serializer.deserialize()
    note = note_book.find_note("personal")
    assert note is not None
    assert note.text.value == "First line of notes"
    assert note_book.find_note("work") is None

    expected = str(note)
    out = capsys.readouterr().out
    assert expected in out
