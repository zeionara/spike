from dataclasses import dataclass
from typing import ClassVar

from .ContextEntry import ContextEntry


@dataclass
class PrefixContextEntry(ContextEntry):
    mark: ClassVar[str] = 'prefix'

    uri: str
    shortcut: str
    trailer: str

    @staticmethod
    def from_dict(prefixes: dict[str, str], trailers: dict[str, str], default: str = '#'):
        entries = []

        for uri, shortcut in prefixes.items():
            entries.append(
                PrefixContextEntry(uri, shortcut, trailers.get(shortcut, default))
            )

        return entries

    @property
    def description(self):
        return f'@prefix {self.shortcut}: <{self.uri}{self.trailer}>'
