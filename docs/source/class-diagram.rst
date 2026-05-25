Class diagram
=============

The diagram shows the structure of the address book application: the base field and specialized
fields, contact record, address book container, birthday processing helper, and persistence
serializer.

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
  
    note for Field "Base class for entry fields."
    note for Birthday "Stores the contact birthday. <br/> Validates format (DD.MM.YYYY). <br/> format() returns DD.MM.YYYY (Weekday)."
    note for Name "Stores the contact name. <br/> Validates that name is a non-empty alphanumeric string."
    note for Phone "Stores the phone number. <br/> Validates format (10 digits)."
    note for Record "Stores contact information: name, phones, and optional birthday. <br/> Invalid name or phone raises ValueError. <br/> Can add, remove, edit, and find phone numbers."
    note for AddressBook "Stores entries keyed by contact name. <br/> get_upcoming_birthdays() returns records with birthdays in the next 7 days."
    note for ProcessedRecord "Wraps a record with a weekend-adjusted congratulation date. <br/> Used to filter and sort upcoming birthdays."
    note for AddressBookSerializer "Persists AddressBook to disk via pickle. <br/> On I/O failure, reports a warning via send_error_message."
Relationships
-------------

* **Field** is the base class; **Name**, **Phone**, and **Birthday** are subclasses.
* **Record** has composition with **Name** (one required name), **Phone** (a list of numbers),
  and **Birthday** (optional, zero or one).
* **AddressBook** has composition with **Record** (a collection of contact entries).
* **AddressBook** uses **ProcessedRecord** when computing upcoming birthdays (filtering and
  sorting by congratulation date).
* **AddressBookSerializer** reads and writes **AddressBook** instances to a file using pickle.
