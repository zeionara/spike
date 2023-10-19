from requests import get


TIMEOUT = 3600  # seconds


class QueryEngine:
    root = 'https://orkg.org/triplestore'

    def __init__(self):
        pass

    def run(self, query: str, id_: str):
        response = get(
            self.root,
            {
                'query': query
            },
            headers = {
                'Accept': 'application/sparql-results+json'
            },
            timeout = TIMEOUT
        )

        try:
            data = response.json()

            return [
                cell['value']
                for row in data['results']['bindings']
                for _, cell in row.items()
            ], True
        except Exception as e:
            print(f'Cannot execute query "{id_}"')
            print(query)
            print(e)

            return [], False
