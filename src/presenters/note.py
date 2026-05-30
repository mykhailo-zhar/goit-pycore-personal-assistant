from io import StringIO

from rich.console import Console
from rich.table import Table

from src.note import Note


class NotePresenter:
    def __init__(self, notes: list[Note] | Note):
        self.notes = notes if isinstance(notes, list) else [notes]

    def __str__(self) -> str:
        """
        Повертає рядкове подання нотатки.

        Повертає:
            str: Рядкове подання нотатки у вигляді таблиці.
        """
        table = Table()
        table.add_column("Title", style="bold")
        table.add_column("Text", style="bold")
        table.add_column("Tags", style="bold")

        for note in self.notes:
            title = note.title if note.title else "None"
            text = note.text if getattr(note, "text", None) else "None"
            tags = note.show_tags()
            table.add_row(str(title), str(text), tags)

        console_file = StringIO()
        console = Console(
            file=console_file,
            force_jupyter=False,
            force_terminal=True,
            color_system=None,
            width=120,
        )
        console.print(table)
        return console_file.getvalue().rstrip()
