from os import path

from urllib.parse import urlencode
import pickle as pkl

from .util import cut_prefix

from requests import get

CONTEXT_EXTRACTION_QUERY = '''
prefix c: <http://orkg.org/orkg/class/>
prefix r: <http://orkg.org/orkg/resource/>

prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#>

select distinct ?class ?label
where {
  ?resource rdf:type ?class.
  ?class rdfs:label ?label
  filter not exists {
    ?class rdfs:label ?label.
    filter regex(?label, "[A-Z]+[0-9]+")
  }
  filter not exists {
    ?class rdfs:label ?label.
    filter regex(?label, "[a-z]+:[A-Z0-9_]+")
  }
}
'''

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


class OrkgContext:
    root = 'https://orkg.org/{path}'

    def __init__(self, cache_path: str = path.join('assets', 'orkg-context.pkl')):
        if path.isfile(cache_path):
            with open(cache_path, 'rb') as file:
                self.context = pkl.load(file)
                return

        response = get(self.triplestore, {'query': CONTEXT_EXTRACTION_QUERY}, headers = {'Accept': 'application/sparql-results+json'})

        context = []

        for uri, shortcut in PREFIXES.items():
            context.append(f'@prefix {shortcut}: <{uri}{TRAILERS[shortcut]}>')

        context.append('')

        for binding in response.json()['results']['bindings']:
            # binding = response.json()['results']['bindings'][0]

            class_ = cut_prefix(binding['class']['value'], PREFIXES)
            label = binding['label']['value']

            context.append(f'{class_} r:label "{label}". _ r:type {class_}.')

        self.context = context

        with open(cache_path, 'wb') as file:
            pkl.dump(context, file)

        # self.description = '\n'.join(context)

        # self.description = self.triplestore.format(query = urlencode({'query': CONTEXT_EXTRACTION_QUERY}))

    def cut(self, phrase: str):
        return '\n'.join([
            line
            for line in self.context
            if 'r:label' not in line or line.split('"')[1].split('"')[0].lower() in phrase.lower()
        ])

    @property
    def description(self):
        return '\n'.join(self.context)

    @property
    def triplestore(self):
        return self.root.format(path = 'triplestore')
