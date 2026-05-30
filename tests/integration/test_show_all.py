import builtins

from main import main
from src.commands.show_all import SHOW_ALL_MESSAGES
from src.serializers.address_book import AddressBookSerializer


def test_show_all_when_no_users(monkeypatch, capsys, tmp_path):
    """Перевіряє виведення повідомлення для порожньої адресної книги.

    Дано:
        Порожня адресна книга.
    Коли:
        Виконується команда ``all``.
    Тоді:
        Виводиться повідомлення про відсутність користувачів.
    """
    lines = iter(
        [
            "all",
            "exit",
        ]
    )
    serializer = AddressBookSerializer(str(tmp_path / "address_book.pkl"))

    monkeypatch.setattr(builtins, "input", lambda: next(lines))
    monkeypatch.setattr(
        "main.SERIALIZER_PATH",
        serializer.file_path,
    )
    main()

    out = capsys.readouterr().out
    assert SHOW_ALL_MESSAGES["NO_USERS"] in out


def test_show_all_displays_full_contact_info(monkeypatch, capsys, tmp_path):
    """Перевіряє виведення повної інформації про контакт.

    Дано:
        Адресна книга з контактом Pat, телефоном та днем народження.
    Коли:
        Виконується команда ``all``.
    Тоді:
        У виводі відображаються ім'я, телефон, день народження та порожні email і адреса.
    """
    lines = iter(
        [
            "add Pat 1234567890",
            "insert-birthday Pat 14.10.1992",
            "all",
            "exit",
        ]
    )
    serializer = AddressBookSerializer(str(tmp_path / "address_book.pkl"))

    monkeypatch.setattr(builtins, "input", lambda: next(lines))
    monkeypatch.setattr(
        "main.SERIALIZER_PATH",
        serializer.file_path,
    )
    main()

    out = capsys.readouterr().out
    assert "Stored users (1):" in out
    assert "Pat" in out
    assert "1234567890" in out
    assert "14.10.1992" in out
    assert "None" in out
    assert "None" in out
