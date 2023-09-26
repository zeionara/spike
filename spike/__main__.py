# from os import path
# from pickle import load, dump

from json import load
from click import group, argument, option

# from openai import ChatCompletion as cc

# from .OrkgContext import OrkgContext
from .similarity import compare as compare_strings, rank
from .SciQA import SciQA
from .Responder import Responder
from .util import drop_spaces


NEW_LINE = '\n'


@group()
def main():
    pass


@main.command()
@argument('question', type = str)
@option('-d', '--dry-run', is_flag = True, help = 'Print generated context and exit')
@option('-f', '--fresh', is_flag = True, help = 'Don\'t use cached context entries, generate them from scratch')
@option('-c', '--cache-path', type = str, help = 'Path to the cached answers', default = 'assets/answers.pkl')
@option('-q', '--questions-path', type = str, help = 'Path to the file with questions', default = None)
def ask(question: str, dry_run: bool, fresh: bool, cache_path: str, questions_path: str):
    responder = Responder(cache_path)

    if questions_path is None:
        answer = responder.ask(question, fresh = fresh, dry_run = dry_run)
        print(answer)
    else:
        with open(questions_path, 'r', encoding = 'utf-8') as file:
            content = load(file)

        n_matched_queries = 0
        n_queries = 0

        for i, entry in enumerate(content):
            question = entry["question"]["string"]

            print(f'{i:03d}. {question}')

            query, answer = responder.ask(question)

            if drop_spaces(query) == drop_spaces(entry['query']['sparql']):
                n_matched_queries += 1
            else:
                print(query)
                print(entry['query']['sparql'])

            if len(answer) > 0:
                print(answer)

            n_queries += 1

        print('precision: ', n_matched_queries / n_queries)

    # cache = None

    # if cache_path is not None and path.isfile(cache_path):
    #     with open(cache_path, 'rb') as file:
    #         cache = load(file)

    # if cache is not None:
    #     answer = cache.get(question)

    #     if answer is not None:
    #         print(answer)
    #         return

    # context = OrkgContext(fresh = fresh)

    # # if dry_run:
    # #     # print(context.description)
    # #     print(context.cut(question))
    # # else:
    # examples, graph = context.cut(question)

    # string_examples = []

    # for example in examples:
    #     string_examples.append(f'Also I know that for a similar question "{example.utterance}" the correct query is \n```\n{example.query}\n```.')

    # # print('\n'.join(string_examples))

    # content = f'''
    # I have a knowledge graph which includes the following fragment:

    # '
    # {graph}
    # '

    # Generate SPARQL query which allows to answer the question "{question}" using this graph

    # {NEW_LINE.join(string_examples)}
    # '''

    # if dry_run:
    #     answer = 'foo'
    # else:
    #     completion = cc.create(
    #         model = 'gpt-3.5-turbo',
    #         messages = [
    #             {
    #                 'role': 'user',
    #                 'content': content
    #             }
    #         ]
    #     )

    #     answer = completion.choices[0].message.content

    # print(answer)

    # if cache_path is not None:
    #     if cache is None:
    #         cache = {question: answer}
    #     else:
    #         cache[question] = answer

    #     with open(cache_path, 'wb') as file:
    #         dump(cache, file)


@main.command()
@argument('lhs', type = str)
@argument('rhs', type = str)
def compare(lhs: str, rhs: str):
    print(f'The similarity of strings "{lhs}" and "{rhs}" is {compare_strings(lhs, rhs)}')


@main.command()
@option('-n', '--top-n', type = int, default = 3)
def trace(top_n: int):
    # print(rank('foo', ['qux', 'o', 'fo'], top_n = 2))

    sciqa = SciQA()

    train_entries = sciqa.train.entries

    for test_utterance in sciqa.test.utterances[:1]:
        print(f'Test sample: {test_utterance}')
        print(f'Similar train samples: {rank(test_utterance, train_entries, top_n, get_utterance = lambda entry: entry.utterance)}')
        print('')

    # print(len(sciqa.train.utterances))
    # print(len(sciqa.test.utterances))


if __name__ == '__main__':
    main()
