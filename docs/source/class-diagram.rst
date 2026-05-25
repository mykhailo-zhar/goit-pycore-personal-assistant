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
    class Record {
      + Name name
      + list~Phone~ phones
      + Birthday|None birthday

      +\__init__(self, name str)
      +add_birthday(birthday str)
      +add_phone(phone str)
      +remove_phone(phone str) bool
      +edit_phone(old_phone, new_phone)
      +find_phone(phone str) Phone|None
      +\__str__(self) str
    }
    class AddressBook {
      + dict data
      + datetime today

      +\__init__(self)
      +add_record(record Record)
      +find_record(name str) Record|None
      +remove_record(name str) bool
      +get_upcoming_birthdays(self) list~Record~
    }
    class ProcessedRecord {
      + Record record
      + datetime congratulation_date

      +\__init__(record, today)
      +is_congratulation_date_in_next_7_days(today)$ Callable
    }
    class AddressBookSerializer {
      + Path file_path
      + Callable send_error_message

      +\__init__(file_path, send_error_message)
      +serialize(address_book) None
      +deserialize() AddressBook
    }

    Field <|-- Name
    Field <|-- Phone
    Field <|-- Birthday

    Record *-- "1" Name : name
    Record *-- "*" Phone : phones
    Record *-- "0..1" Birthday : birthday

    AddressBook *-- "*" Record : records
    AddressBook ..> ProcessedRecord : uses
    ProcessedRecord --> Record : wraps

    AddressBookSerializer ..> AddressBook : serialize / deserialize

    note for Field "Базовий клас полів запису."
    note for Birthday "День народження контакту. <br/> Формат DD.MM.YYYY. <br/> format() повертає DD.MM.YYYY (День тижня)."
    note for Name "Ім'я контакту. <br/> Непорожній алфавітно-цифровий рядок."
    note for Phone "Номер телефону. <br/> Рівно 10 цифр."
    note for Record "Контакт: ім'я, телефони, опційний день народження. <br/> Невалідні дані — ValueError. <br/> Додавання, видалення, редагування телефонів."
    note for AddressBook "Записи за іменем контакту. <br/> get_upcoming_birthdays() — ДН у наступні 7 днів."
    note for ProcessedRecord "Запис із датою привітання з урахуванням вихідних. <br/> Фільтрація та сортування найближчих ДН."
    note for AddressBookSerializer "Збереження AddressBook через pickle. <br/> При помилці I/O — попередження через send_error_message."

Зв'язки
-------

* **Field** — базовий клас; **Name**, **Phone**, **Birthday** — підкласи.
* **Record** містить **Name** (один), **Phone** (список) та **Birthday** (опційно).
* **AddressBook** зберігає колекцію **Record**.
* **AddressBook** використовує **ProcessedRecord** для найближчих днів народження.
* **AddressBookSerializer** читає та записує **AddressBook** у файл через pickle.
