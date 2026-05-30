from src.note import Note


class NotePresenter:
    def __init__(self, note: Note):
        self.note = note

    def __str__(self) -> str:
        return str(self.note)
