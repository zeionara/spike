from abc import ABC, abstractmethod
from typing import ClassVar
from os import path
from dataclasses import dataclass

import pickle as pkl

from .util import cut_prefix, read

from requests import get

PREFIXES = {
    'http://www.w3.org/2002/07/owl': 'w',
    # 'http://www.w3.org/2000/01/rdf-schema': 'r',
    'http://orkg.org/orkg/class': 'c',
    'http://www.w3.org/1999/02/22-rdf-syntax-ns': 'r'
}

TRAILERS = {
    'w': '#',
    'r': '#',
    'c': '/'
}


class ContextEntry(ABC):
    mark: ClassVar[str] = None

    @property
    @abstractmethod
    def description(self):
        pass


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


@dataclass
class ClassContextEntry(ContextEntry):
    mark: ClassVar[str] = 'class'

    prefix: str
    name: str
    label: str

    # def __init__(self, uri: str, label: str, prefixes: dict[str, str]):
    #     self.name = cut_prefix(uri, prefixes)
    #     self.label = label

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
        return f'{self.prefix}:{self.name} r:label {self.label}. _ r:type {self.prefix}:{self.name}'


class OrkgContext:
    root = 'https://orkg.org/{path}'

    def __init__(self, cache_path: str = path.join('assets', 'cache', 'orkg-context.pkl'), fresh: bool = False):
        # 1. Try loading the context entries from cache

        if not fresh and path.isfile(cache_path):
            with open(cache_path, 'rb') as file:
                self.context = pkl.load(file)
                return

        # 2. Get class context data from the knowledge graph

        response = self.get_triples(
            read('assets/queries/classes.rq')
        )

        # 3. Generate context entries

        # context = []

        # for uri, shortcut in PREFIXES.items():
        #     context.append(f'@prefix {shortcut}: <{uri}{TRAILERS[shortcut]}>')

        # context.append('')

        context = PrefixContextEntry.from_dict(PREFIXES, TRAILERS)

        context.append(None)

        for binding in response.json()['results']['bindings']:
            context.append(ClassContextEntry.from_binding(binding, prefixes = PREFIXES))
            # class_ = cut_prefix(binding['class']['value'], PREFIXES)
            # label = binding['label']['value']

            # context.append(f'{class_} r:label "{label}". _ r:type {class_}.')

        self.context = context

        print(context[:10])

        with open(cache_path, 'wb') as file:
            pkl.dump(context, file)

    def cut(self, phrase: str, matches: callable = lambda entry, phrase: entry.label.lower() in phrase.lower()):
        return '\n'.join([
            '' if entry is None else entry.description
            for entry in self.context
            if (
                entry is None or
                entry.mark != 'class' or
                matches(entry, phrase)
            )
            # if 'r:label' not in line or line.split('"')[1].split('"')[0].lower() in phrase.lower()
        ])

    @property
    def description(self):
        return '\n'.join(self.context)

    @property
    def triplestore(self):
        return self.root.format(path = 'triplestore')

    def get_triples(self, query: str):
        return get(self.triplestore, {'query': query}, headers = {'Accept': 'application/sparql-results+json'})
