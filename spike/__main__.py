from click import group, argument


@group()
def main():
    pass


@main.command()
@argument('question', type = str)
def ask(question):
    print(question)


if __name__ == '__main__':
    main()
