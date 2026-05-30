Діаграма класів
===============

Діаграма показує структуру застосунку адресної книги: базове поле та спеціалізовані
поля, запис контакту, контейнер адресної книги, обробник днів народження та серіалізатор.

.. mermaid::
  
  classDiagram
    direction TB

    class Field {
      + value
      +\__init__(self, value)
      +validate(self) bool*
      +\__str__(self) str
    }

    class Name {
      +validate(self) bool
    }
    class Phone {
      +validate(self) bool
    }
    class Birthday {
      +DATE_FORMAT str$
      +validate(self) bool
      +format(today) str
    }
    class Address
    class Email {
      +validate(self) bool
    }
    class Tag {
      +validate(self) bool
    }
    class Title{
      +validate(self) bool
    }
    class Text
    class Record {
      + Name name
      + list~Phone~ phones
      + Birthday|None birthday

      +\__init__(self, name str)
      +add_phone(phone str)
      +remove_phone(phone str) bool
      +find_phone(phone str) Phone|None
      +edit_phone(old_phone, new_phone)
      +add_birthday(birthday str)
      +add_address(address str)
      +add_email(email str)
      +\__str__(self) str
    }
    class AddressBook {
      + dict data
      + datetime today

      +\__init__(self)
      +add_record(record Record)
      +find_record(name str) Record|None
      +remove_record(name str) bool
      +get_upcoming_birthdays(self) list
    }

    
    class Note {
      + title Title
      + text Text
      + tags list~Tag~

      +\__init__(title str)
      + edit_title(title str)
      + add_tag(tag str)
      + remove_tag(tag str) bool
      + show_tags() str
      +\__str__(self) str
    }

    class NotesBook {
      + dict data

      +\__init__(self)
      +add_note(note Note)
      +find_note(title str) Note|None
      +change_note(title str, note Note) bool
      +remove_note(title str) bool
      +show_notes() str
      +search_notes(tag str, order str) list
      +\__str__(self) str
    }

    class PickleSerializer~T~ {
      + Path file_path
      + Callable send_error_message

      +\__init__(file_path, send_error_message)
      +serialize(data T) None
      +deserialize() T
    }
    class NotesBookSerializer
    class AddressBookSerializer

    class NotePresenter {
      +\__init__(notes list~Note~ | Note)
      +\__str__(self) str
    }
    class RecordPresenter {
      +\__init__(records list~Record~ | Record)
      +\__str__(self) str
    }

    Field <|-- Name
    Field <|-- Phone
    Field <|-- Birthday
    Field <|-- Address
    Field <|-- Email
    Field <|-- Tag
    Field <|-- Title
    Field <|-- Text
    PickleSerializer <|-- NotesBookSerializer : implements PickleSerializer~NotesBook~
    PickleSerializer <|-- AddressBookSerializer : implements PickleSerializer~AddressBook~

    Record *-- "1" Name : name
    Record *-- "*" Phone : phones
    Record *-- "0..1" Birthday : birthday

    Note *-- "1" Title : title
    Note *-- "0..1" Text : text
    Note *-- "*" Tag : tags

    AddressBook *-- "*" Record : records
    AddressBook ..> ProcessedRecord : uses

    NotesBook *-- "*" Note : notes

    AddressBookSerializer ..> AddressBook : serialize / deserialize
    NotesBookSerializer ..> NotesBook : serialize / deserialize

    note for Field "Базовий клас полів запису."
    note for Birthday "День народження контакту. <br/> Формат DD.MM.YYYY. <br/> format() повертає DD.MM.YYYY (День тижня)."
    note for Name "Ім'я контакту. <br/> Непорожній алфавітно-цифровий рядок."
    note for Phone "Номер телефону. <br/> Рівно 10 цифр."
    note for Email "Email. <br/> Валідна email адреса."
    note for Title "Заголовок нотатки. <br/> Непорожній алфавітно-цифровий рядок до 100 символів."
    note for Tag "Тег нотатки. <br/> Непорожній алфавітно-цифровий рядок до 30 символів."
    note for Record "Контакт: ім'я, телефони, опційний день народження. <br/> Невалідні дані — ValueError. <br/> Додавання, видалення, редагування телефонів."
    note for AddressBook "Записи за іменем контакту. <br/> get_upcoming_birthdays() — ДН у наступні 7 днів."
    note for ProcessedRecord "Запис із датою привітання з урахуванням вихідних. <br/> Фільтрація та сортування найближчих ДН."
    note for PickleSerializer "Збереження T через pickle. <br/> При помилці I/O — попередження через send_error_message."

Зв'язки
-------

* **Field** — базовий клас; **Name**, **Phone**, **Birthday** — підкласи.
* **Record** містить **Name** (один), **Phone** (список) та **Birthday** (опційно).
* **AddressBook** зберігає колекцію **Record**.
* **AddressBook** використовує **ProcessedRecord** для найближчих днів народження.
* **AddressBookSerializer** читає та записує **AddressBook** у файл через pickle.
