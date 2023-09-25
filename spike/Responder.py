from time import sleep
from os import path
from pickle import load, dump

from openai import ChatCompletion as cc

from .OrkgContext import OrkgContext


NEW_LINE = '\n'

# PROMPT = '''
# I have a knowledge graph which includes the following fragment:
#
# '
# {graph}
# '
#
# Generate SPARQL query which allows to answer the question "{question}" using this graph
#
# {examples}
# '''

PROMPT = '''
Generate SPARQL query which allows to answer the question "{question}".

{examples}
'''


class Responder:
    def __init__(self, cache_path: str):
        cache = None

        if cache_path is not None and path.isfile(cache_path):
            with open(cache_path, 'rb') as file:
                cache = load(file)

        self.cache_path = cache_path
        self.cache = cache

    def _extract_query(self, answer: str):
        parts = answer.replace('```sparql', '```').split('```')

        if len(parts) != 3:
            return answer
            # raise ValueError(f'Can\'t extract query from answer "{answer}"')

        return parts[1]

    def _execute(self, answer: str, context: OrkgContext):
        query = self._extract_query(answer)

        # print(query)

        return query, context.get_triples(query)

    def ask(self, question: str, fresh: bool = False, dry_run: bool = False):
        cache = self.cache

        context = OrkgContext(fresh = fresh)

        if cache is not None and not dry_run:
            answer = cache.get(question)

            if answer is not None:
                return self._execute(answer, context)

        # examples, graph = context.cut(question)
        examples, _ = context.cut(question)

        string_examples = []

        for example in examples:
            # string_examples.append(f'Also I know that for a similar question "{example.utterance}" the correct query is \n```\n{example.query}\n```.')
            string_examples.append(f'I know that for a similar question "{example.utterance}" the correct query is \n```\n{example.query}\n```.')

        # content = PROMPT.format(graph = graph, examples = NEW_LINE.join(string_examples))
        content = PROMPT.format(examples = NEW_LINE.join(string_examples), question = question)

        if dry_run:
            answer = content
        else:
            completion = cc.create(
                model = 'gpt-3.5-turbo',
                messages = [
                    {
                        'role': 'user',
                        'content': content
                    }
                ]
            )

            sleep(20)

            answer = completion.choices[0].message.content

        cache_path = self.cache_path

        if cache_path is not None:
            if cache is None:
                cache = {question: answer}
            else:
                cache[question] = answer

            with open(cache_path, 'wb') as file:
                dump(cache, file)

        return self._execute(answer, context)
