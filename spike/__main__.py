from click import group, argument

from openai import ChatCompletion as cc


@group()
def main():
    pass


@main.command()
@argument('question', type = str)
def ask(question: str):
    completion = cc.create(
        model = 'gpt-3.5-turbo',
        messages = [
            {
                'role': 'user',
                'content': f'''
                I have the following knowledge graph:

                '
                @prefix mco: <http://kgrl.org/mco#> .

                mco:foo mco:friend mco:bar; mco:baz.

                mco:foo mco:age 17.
                '

                Generate SPARQL query which allows to answer the question "{question}" using this graph
                '''
            }
        ]
    )

    print(completion.choices[0].message.content)


if __name__ == '__main__':
    main()
