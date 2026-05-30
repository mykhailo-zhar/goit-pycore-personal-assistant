from io import StringIO

from rich.console import Console
from rich.table import Table

from src.record import Record


class RecordPresenter:
    def __init__(self, records: list[Record] | Record):
        self.records = records if isinstance(records, list) else [records]

    def __str__(self) -> str:
        # Using Rich for table rendering, but Rich import is assumed to be handled outside this method.

        table = Table()
        table.add_column("Name", style="bold")
        table.add_column("Phones", style="bold")
        table.add_column("Email", style="bold")
        table.add_column("Birthday", style="bold")
        table.add_column("Address", style="bold")

        for record in self.records:
            name = record.name.value
            phones = ", ".join(p.value for p in record.phones) or "None"
            email = record.email.value if record.email else "None"
            birthday = record.birthday.value if record.birthday else "None"
            address = record.address.value if record.address else "None"
            table.add_row(str(name), phones, email, birthday, address)

        # Render table to string
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
