from click import group, argument, option

from openai import ChatCompletion as cc

from .OrkgContext import OrkgContext
from .similarity import compare as compare_strings, rank
from .SciQA import SciQA


@group()
def main():
    pass


@main.command()
@argument('question', type = str)
@option('-d', '--dry-run', is_flag = True, help = 'Print generated context and exit')
@option('-f', '--fresh', is_flag = True, help = 'Don\'t use cached context entries, generate them from scratch')
def ask(question: str, dry_run: bool, fresh: bool):
    context = OrkgContext(fresh = fresh)

    if dry_run:
        # print(context.description)
        print(context.cut(question))
    else:
        completion = cc.create(
            model = 'gpt-3.5-turbo',
            messages = [
                {
                    'role': 'user',
                    'content': f'''
                    I have a knowledge graph which includes the following fragment:

                    '
                    {context.cut(question)}
                    '

                    Generate SPARQL query which allows to answer the question "{question}" using this graph
                    '''
                }
            ]
        )

        print(completion.choices[0].message.content)


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
