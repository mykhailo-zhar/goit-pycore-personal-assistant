import builtins

from main import main
from src.utils.serializers.note_book import NoteBookSerializer


def test_tag_workflow(monkeypatch, capsys, tmp_path):
    """Перевіряє повний цикл роботи з тегами.

    Дано:
        Порожня книга нотаток.
    Коли:
        Послідовно виконуються команди ``add-note``, ``add-tag``,
        ``tag``, ``remove-tag`` та повторний ``tag``.
    Тоді:
        У нотатці залишається лише тег ``urgent``,
        у виводі з'являється рядкове подання нотатки.
    """
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
        "main.NOTE_SERIALIZER_PATH",
        note_serializer.file_path,
    )
    main()

    note = note_serializer.deserialize().find_note("ideas")
    assert note.show_tags() == "urgent"

    out = capsys.readouterr().out
    assert str(note) in out
