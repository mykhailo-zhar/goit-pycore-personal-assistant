import builtins

from src.commands.show_all import SHOW_ALL_MESSAGES
from src.scripts.contacts_bot import main
from src.utils.address_book_serializer import AddressBookSerializer


def test_show_all_when_no_users(monkeypatch, capsys, tmp_path):
    lines = iter(
        [
            "all",
            "exit",
        ]
    )
    serializer = AddressBookSerializer(str(tmp_path / "address_book.pkl"))

    monkeypatch.setattr(builtins, "input", lambda: next(lines))
    monkeypatch.setattr(
        "src.scripts.contacts_bot.SERIALIZER_PATH",
        serializer.file_path,
    )
    main()

    out = capsys.readouterr().out
    assert SHOW_ALL_MESSAGES["NO_USERS"] in out


def test_show_all_displays_full_contact_info(monkeypatch, capsys, tmp_path):
    lines = iter(
        [
            "add Pat 1234567890",
            "add-birthday Pat 14.10.1992",
            "all",
            "exit",
        ]
    )
    serializer = AddressBookSerializer(str(tmp_path / "address_book.pkl"))

    monkeypatch.setattr(builtins, "input", lambda: next(lines))
    monkeypatch.setattr(
        "src.scripts.contacts_bot.SERIALIZER_PATH",
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
