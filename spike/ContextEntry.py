from abc import ABC, abstractmethod
from typing import ClassVar


class ContextEntry(ABC):
    mark: ClassVar[str] = None

    @property
    @abstractmethod
    def description(self):
        pass
