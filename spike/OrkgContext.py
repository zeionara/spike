from os import path
import pickle as pkl

from rdflib import Graph
from pyparsing.exceptions import ParseException

from .util import read

from .ClassContextEntry import ClassContextEntry
from .PrefixContextEntry import PrefixContextEntry
from .PropertyContextEntry import PropertyContextEntry
from .SciQA import SciQA
from .similarity import rank

from requests import get
from requests.exceptions import JSONDecodeError

HEADER = '''
prefix orkgp: <http://orkg.org/orkg/predicate/>
prefix orkgc: <http://orkg.org/orkg/class/>
prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#>
'''

PREFIXES = {
    'http://www.w3.org/2002/07/owl': 'w',
    # 'http://www.w3.org/2000/01/rdf-schema': 'r',
    'http://orkg.org/orkg/class': 'c',
    'http://orkg.org/orkg/predicate': 'p',
    'http://www.w3.org/1999/02/22-rdf-syntax-ns': 'r'
}

TRAILERS = {
    'w': '#',
    'r': '#',
    'c': '/'
}


class OrkgContext:
    root = 'https://orkg.org/{path}'

    def __init__(self, cache_path: str = path.join('assets', 'cache', 'orkg-context.pkl'), fresh: bool = False, graph: Graph = None):
        self.graph = graph

        # 0. Read SciQA dataset (which caches itself)

        self.sciqa = SciQA()

        # 1. Try loading the context entries from cache

        if not fresh and path.isfile(cache_path):
            with open(cache_path, 'rb') as file:
                self.context = pkl.load(file)
                return

        # 2. Get class context data from the knowledge graph

        classes = self.get_triples(
            read('assets/queries/classes.rq')
        )

        properties = self.get_triples(
            read('assets/queries/properties.rq')
        )

        # 3. Generate context entries

        context = PrefixContextEntry.from_dict(PREFIXES, TRAILERS)

        context.append(None)

        for binding in classes:
            context.append(ClassContextEntry.from_binding(binding, prefixes = PREFIXES))

        for binding in properties:
            context.append(PropertyContextEntry.from_binding(binding, prefixes = PREFIXES))

        self.context = context

        with open(cache_path, 'wb') as file:
            pkl.dump(context, file)

    def cut(self, phrase: str, matches: callable = lambda entry, phrase: entry.label.lower() in phrase.lower()):
        examples = rank(phrase, self.sciqa.train.entries, top_n = 3, get_utterance = lambda entry: entry.utterance)

        return examples, '\n'.join([
            '' if entry is None else entry.description
            for entry in self.context
            if (
                entry is None or
                entry.mark == PrefixContextEntry.mark or
                matches(entry, phrase)
            )
        ])

    @property
    def description(self):
        return '\n'.join(self.context)

    @property
    def triplestore(self):
        return self.root.format(path = 'triplestore')

    def get_triples(self, query: str):
        # prefixes = PrefixContextEntry.from_dict(PREFIXES, TRAILERS)
        # header = '\n'.join([prefix.description for prefix in prefixes])

        query = f'{HEADER}\n{query}'

        # print(query)

        if self.graph is None:
            response = get(self.triplestore, {'query': query}, headers = {'Accept': 'application/sparql-results+json'}, timeout = 120)

            # print(response.text)

            try:
                return response.json()['results']['bindings']
            except JSONDecodeError:
                print(f'Cannot extract entries from response {response.text}. Returning an empty list...')
                return []
        else:
            try:
                response = self.graph.query(query)
            except Exception:
                print('Cannot execute query!!!')
                print(query)

                return []

            return [
                str(cell)
                for row in response
                for cell in row
            ]
