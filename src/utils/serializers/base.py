from abc import ABC, abstractmethod
from typing import Any


class Serializer(ABC):
    """
    Базовий клас для серіалізаторів.

    Аргументи:
        ABC: Базовий клас для абстрактних класів.
    """

    @abstractmethod
    def serialize(self, object: Any) -> None:
        """
        Серіалізує об'єкт.

        Аргументи:
            object: Об'єкт для серіалізації.
        """
        pass

    @abstractmethod
    def deserialize(self, object: Any) -> Any:
        """
        Десеріалізує об'єкт.

        Аргументи:
            object: Об'єкт для десеріалізації.
        """
        pass
