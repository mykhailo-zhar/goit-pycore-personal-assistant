from io import StringIO

from rich.console import Console
from rich.table import Table

from src.note import Note


class NotePresenter:
    def __init__(self, notes: list[Note] | Note):
        self.notes = notes if isinstance(notes, list) else [notes]

    def __str__(self) -> str:

        table = Table()
        table.add_column("Title", style="bold")
        table.add_column("Text", style="bold")
        table.add_column("Tags", style="bold")

        for note in self.notes:
            title = note.title.value if note.title else "None"
            text = note.text.value if note.text else "None"
            tags = ", ".join(tag.value for tag in note.tags) if note.tags else "None"
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
