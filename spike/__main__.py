from click import group, argument, option

from openai import ChatCompletion as cc

from .OrkgContext import OrkgContext


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


if __name__ == '__main__':
    main()
