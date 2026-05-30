from src.record import Record


class RecordPresenter:
    def __init__(self, record: Record):
        self.record = record

    def __str__(self) -> str:
        return str(self.record)
