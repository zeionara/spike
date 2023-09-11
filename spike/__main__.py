from click import group, argument

from openai import ChatCompletion as cc

from .OrkgContext import OrkgContext


@group()
def main():
    pass


@main.command()
@argument('question', type = str)
def ask(question: str):
    context = OrkgContext()

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
