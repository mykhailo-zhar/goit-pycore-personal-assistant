import builtins

from src.scripts.contacts_bot import main
from src.utils.serializers.note_book import NoteBookSerializer


def test_tag_workflow(monkeypatch, capsys, tmp_path):
    """Перевіряє повний цикл роботи з тегами."""
    note_serializer = NoteBookSerializer(str(tmp_path / "notebook.pkl"))
    lines = iter(
        [
            "add-note ideas",
            "add-tag ideas urgent",
            "add-tag ideas work",
            "tag urgent ascending",
            "remove-tag ideas work",
            "tag urgent descending",
            "exit",
        ]
    )
    monkeypatch.setattr(builtins, "input", lambda: next(lines))
    monkeypatch.setattr(
        "src.scripts.contacts_bot.NOTE_SERIALIZER_PATH",
        note_serializer.file_path,
    )
    main()

    note = note_serializer.deserialize().find_note("ideas")
    assert note.show_tags() == "urgent"

    out = capsys.readouterr().out
    assert str(note) in out
