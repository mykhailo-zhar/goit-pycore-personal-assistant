# goit-pycore-hw-08

Бот-асистент контактів на OOP: `Record`, `AddressBook`, типізовані поля (`Name`, `Phone`, `Birthday`). Дані зберігаються між сесіями через pickle ([`AddressBookSerializer`](src/utils/address_book_serializer.py)). Точка входу — [`main.py`](main.py), CLI — [`src/scripts/contacts_bot.py`](src/scripts/contacts_bot.py).

## Запуск

```bash
uv sync
uv run python main.py
```

Одна команда на рядок; завершення — `exit` або `close`. Файл даних за замовчуванням: **`addressbook.pkl`** у поточній директорії.

## Команди

| Команда | Синтаксис | Успішна відповідь | Зберігає |
|---------|-----------|-------------------|----------|
| hello | `hello` | `How can I help you?` | — |
| add | `add <ім'я> <телефон>` | `Contact added.` | так |
| update | `update <ім'я> <телефон>` | `Contact updated.` | так |
| phone | `phone <ім'я>` | номер(и) через `; ` | — |
| all | `all` | список користувачів | — |
| add-birthday | `add-birthday <ім'я> DD.MM.YYYY` | підтвердження | так |
| show-birthday | `show-birthday <ім'я>` | дата народження | — |
| birthdays | `birthdays` | найближчі ДН (7 днів) | — |
| exit / close | `exit` | `Good bye!` | — |

Телефон — 10 цифр; дата народження — `DD.MM.YYYY`. Команди нечутливі до регістру.

## Серіалізація

При старті бот завантажує `addressbook.pkl` (якщо є); після `add`, `update`, `add-birthday` — зберігає книгу. Помилки I/O лише виводяться як попередження. Деталі — [`address_book_serializer.py`](src/utils/address_book_serializer.py), тести — [`tests/address_book/test_serializer.py`](tests/address_book/test_serializer.py).

## Розробка

Потрібні [mise](https://mise.jdx.dev/) та Python 3.12 ([mise.toml](mise.toml)):

```bash
mise trust && mise install
uv sync
mise run pre-commit-install   # один раз на клон
```

| Задача | Команда |
|--------|---------|
| Тести | `mise run test` |
| Лінт | `mise run lint` |
| Збірка HTML-доків | `mise run build-docs` |
| Регенерація apidoc | `mise run generate-docs` |

**Документація:** HTML у `docs/build/`. Після `generate-docs` заголовки в `.rst` перезаписуються англійською — локалізуйте їх знову або не регенеруйте без потреби.

**CI:** тести на PR/push до `main` / `master` — [`.github/workflows/tests.yml`](.github/workflows/tests.yml).

## Ліцензія

[LICENSE](LICENSE)
