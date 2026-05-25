# goit-pycore-hw-08

GoIT Python core homework: a **contact helper bot** built with OOP (`Record`, `AddressBook`, typed `Field` subclasses for name, phone, and birthday). Contacts are **persisted between sessions** with pickle via [`AddressBookSerializer`](src/utils/address_book_serializer.py). The CLI lives in [`src/scripts/contacts_bot.py`](src/scripts/contacts_bot.py); [`main.py`](main.py) is the app entry point.

Tooling around the project (unchanged):

- [mise](https://mise.jdx.dev/) for tool versions and tasks
- [uv](https://docs.astral.sh/uv/) for dependencies and the virtual environment
- [pytest](https://pytest.org/) for tests
- [ruff](https://docs.astral.sh/ruff/) for linting
- [pre-commit](https://pre-commit.com/) for git hooks
- [Sphinx](https://www.sphinx-doc.org/) for documentation

**CI:** pull requests and pushes to `main` / `master` run tests via [`.github/workflows/tests.yml`](.github/workflows/tests.yml).

## Features

- **Contacts:** add phone numbers, update a contact’s phones, list one user’s phones or all users.
- **Birthdays:** store `DD.MM.YYYY` per contact, show one contact’s birthday, list upcoming birthdays (next 7 days) using weekend-adjusted “congratulation” dates from `AddressBook.get_upcoming_birthdays()`.
- **Persistence:** on startup the bot loads `addressbook.pkl` (if present); after mutating commands it saves the in-memory `AddressBook` back to that file. See [Serialization](#serialization) below.
- **Input:** commands are case-insensitive; the first token is the command, the rest are arguments (whitespace-separated).
- **Errors:** invalid input and domain errors are turned into user-visible strings (via `input_error`); unknown commands get `Invalid command.`.

## Run the bot

From the repository root (after `uv sync`):

```bash
uv run python main.py
```

Or:

```bash
uv run python -m src.scripts.contacts_bot
```

Type one command per line; the bot prints the reply and waits for the next line until you run `exit` or `close`.

The default storage file is **`addressbook.pkl`** in the current working directory (see `SERIALIZER_PATH` in [`src/scripts/contacts_bot.py`](src/scripts/contacts_bot.py)).

## Serialization

[`AddressBookSerializer`](src/utils/address_book_serializer.py) reads and writes an `AddressBook` with Python’s `pickle` module.

| Method | Role |
|--------|------|
| `__init__(file_path, send_error_message=...)` | Stores the target path. Raises `FileNotFoundError` if `file_path` is a directory. Optional `send_error_message` callback receives warning strings on I/O failure. |
| `deserialize()` | Loads the book from disk. On missing file, permission error, or other read failure: calls `send_error_message`, returns an empty `AddressBook`. |
| `serialize(address_book)` | Writes the book to disk. On write failure: calls `send_error_message`; does not raise. |

**Bot integration** ([`contacts_bot.py`](src/scripts/contacts_bot.py)):

1. `main()` builds `AddressBookSerializer("addressbook.pkl", print)` and calls `deserialize()` before the REPL loop.
2. The `serializes` decorator wraps handlers that change data and calls `serializer.serialize(book)` after a successful command.
3. Commands wrapped with `serializes` (save after success): `add`, `update`, `add-birthday`, `show-birthday`. Read-only commands (`hello`, `phone`, `all`, `birthdays`) do not save.
4. `exit` / `close` end the session without an extra save (data was already written on the last mutating command).

To use the serializer outside the bot:

```python
from src.address_book import AddressBook
from src.utils.address_book_serializer import AddressBookSerializer

serializer = AddressBookSerializer("addressbook.pkl")
book = serializer.deserialize()
# ... modify book ...
serializer.serialize(book)
```

Tests: [`tests/address_book/test_serializer.py`](tests/address_book/test_serializer.py), integration coverage in [`tests/contacts_bot/test_integration.py`](tests/contacts_bot/test_integration.py).

## Command reference

| Command | Syntax | Typical success reply | Notes |
|--------|--------|------------------------|--------|
| **hello** | `hello` | `How can I help you?` | No extra arguments. |
| **add** | `add <name> <phone>` | `Contact added.` | Phone must be **10 digits**. If the name already exists, another phone is added to that contact. **Saves** to `addressbook.pkl`. |
| **update** | `update <name> <phone>` | `Contact updated.` | Replaces phones for that user with the given phone. `No such user` if missing. **Saves** to `addressbook.pkl`. |
| **phone** | `phone <name>` | Phone number(s), joined with `; ` | `No such user` if missing. |
| **all** | `all` | `Stored users (<n>):` then lines `Name: phone; phone` | `There are no users` if the book is empty. |
| **add-birthday** | `add-birthday <name> <DD.MM.YYYY>` | Birthday confirmation message | `No such user` if missing. Invalid date → validation error text. **Saves** to `addressbook.pkl`. |
| **show-birthday** | `show-birthday <name>` | `Birthday for <name> is <DD.MM.YYYY>` | `No such user` or `No birthday set for <name>` when applicable. |
| **birthdays** | `birthdays` | `Upcoming birthdays:` then lines **`<DD.MM.YYYY> (<Weekday>) <Name>`** | `There are no users` if the book is empty. No arguments. |
| **exit** / **close** | `exit` or `close` | `Good bye!` | Ends the session. No arguments. |

**Birthday format:** `DD.MM.YYYY` (see [`src/fields/birthday.py`](src/fields/birthday.py)).

## Prerequisites

- [mise](https://mise.jdx.dev/getting-started.html) installed and activated in your shell (for example `eval "$(mise activate bash)"` for Bash).

Python is pinned via [mise.toml](mise.toml) (default **3.12**, overridable with `PYTHON_VERSION`). The repo also carries [.python-version](.python-version) for tooling that reads it.

## Quick start

1. **Trust and install tools** (from the repo root):

   ```bash
   mise trust
   mise install
   ```

   This installs **Python**, **uv**, and **ruff**, and with `python.uv_venv_auto` manages [.venv](.venv).

2. **Install dependencies** (from [pyproject.toml](pyproject.toml) + [uv.lock](uv.lock)):

   ```bash
   uv sync
  ```
3. **Install pre-commit hooks** (once per clone, after `uv sync`):
  ```bash
   mise run pre-commit-install
  ```
4. **Add a new dependency** (updates `pyproject.toml` and `uv.lock`):
  ```bash
   uv add <package>
   ```

   Or use the mise task (see `mise run install --help` for argument passing on your mise version).

## Layout

- **`src/`** — application code (document with docstrings; Sphinx autodoc is configured in [docs/source/conf.py](docs/source/conf.py) with the project root and `src/` on `sys.path`). Includes [`src/utils/address_book_serializer.py`](src/utils/address_book_serializer.py) for pickle persistence.
- **`tests/`** — tests; run with pytest.
- **`docs/`** — documentation; generated by Sphinx.

## Common commands

| Goal | Command |
|------|---------|
| Run tests | `mise run test` or `uv run pytest tests/` |
| Lint `src/` | `mise run lint` |
| Project / venv info | `mise run info` |
| Regenerate Sphinx API stubs | `mise run generate-docs` (`mise run gd`) |
| Build HTML docs | `mise run build-docs` (`mise run bd`) |

| Goal                        | Command                                   |
| --------------------------- | ----------------------------------------- |
| Run tests                   | `mise run test` or `uv run pytest tests/` |
| Lint `src/`                 | `mise run lint`                           |
| Project / venv info         | `mise run info`                           |
| Regenerate Sphinx API stubs | `mise run generate-docs` (`mise run gd`)  |
| Build HTML docs             | `mise run build-docs` (`mise run bd`)     |
| Install pre-commit hooks    | `mise run pre-commit-install`             |


HTML output goes to `**docs/build/**` (open `docs/build/index.html` after a build).

After `sphinx-apidoc` adds `.rst` files under [docs/source](docs/source), include them in the `toctree` in [docs/source/index.rst](docs/source/index.rst) so they appear in the built site.

## Workflow

1. Configure mise, run `**uv sync**`, then `**mise run pre-commit-install**`.
2. Implement code under `**src/**` and tests under `**tests/**`, using docstrings where useful.
3. Run `**mise run lint**` and `**mise run test**`.
4. Run `**mise run generate-docs**` then `**mise run build-docs**` when you want refreshed API documentation.

## License

See [LICENSE](LICENSE).
