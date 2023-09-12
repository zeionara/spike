from dataclasses import dataclass
from typing import ClassVar

from .ContextEntry import ContextEntry
from .util import cut_prefix


@dataclass
class ClassContextEntry(ContextEntry):
    mark: ClassVar[str] = 'class'

    prefix: str
    name: str
    label: str

    @classmethod
    def from_binding(cls, binding: dict, prefixes: dict[str, str]):
        prefix, name = cut_prefix(binding['class']['value'], prefixes)

        return ClassContextEntry(
            prefix = prefix,
            name = name,
            label = binding['label']['value']
        )

    @property
    def description(self):
        return f'{self.prefix}:{self.name} r:label {self.label}. _ r:type {self.prefix}:{self.name}.'
