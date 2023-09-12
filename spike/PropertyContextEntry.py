from dataclasses import dataclass
from typing import ClassVar

from .ContextEntry import ContextEntry
from .util import cut_prefix


@dataclass
class PropertyContextEntry(ContextEntry):
    mark: ClassVar[str] = 'property'

    prefix: str
    name: str
    label: str

    @classmethod
    def from_binding(cls, binding: dict, prefixes: dict[str, str]):
        prefix, name = cut_prefix(binding['property']['value'], prefixes)

        return PropertyContextEntry(
            prefix = prefix,
            name = name,
            label = binding['label']['value']
        )

    @property
    def description(self):
        return f'{self.prefix}:{self.name} r:label {self.label}. _ {self.prefix}:{self.name} _.'
