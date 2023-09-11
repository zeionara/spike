# spike

**SP**ARQL **i**ntelligence for **k**nowlege **e**xtraction (spike) - a tool for generating sparql queries from natural language utterances using large machine learning models

## Set up environment

To install dependencies use the provided `.yml` file:

```sh
conda env create -f environment.yml
```

## Run the app

To ask the tool to generate a sparql query, run the following command:

```sh
python -m spike ask 'What kind of bear is best'
```

For example, the following are some answers from the bot:

````sh
To answer the question "How old is foo" using the given knowledge graph, you can use the following SPARQL query:

PREFIX mco: <http://kgrl.org/mco#>

```sparql
SELECT ?age
WHERE {
  mco:foo mco:age ?age .
}
```

This query selects the `?age` value for `mco:foo` using the `mco:age` property. By executing this query, you will get the age of foo as the result.
````

````sh
The SPARQL query to answer the question "How many friends does foo have?" using the given graph is as follows:

```
PREFIX mco: <http://kgrl.org/mco#>

SELECT (COUNT(?friend) AS ?numFriends)
WHERE {
  mco:foo mco:friend ?friend .
}
```


This query uses the `COUNT` function to count the number of `friend` relationships for the resource `mco:foo`. The result variable is named `numFriends`.
````

## Open ai response example

Open ai server responds with the following object:

```json
{
  "choices": [
    {
      "finish_reason": "stop",
      "index": 0,
      "message": {
        "content": "There isn't a clear answer to this question as opinions may vary. Some people might argue that the grizzly bear is the best due to its strength and size, while others might say the polar bear is the best because of its adaptability to extreme cold environments. Ultimately, the \"best\" bear depends on personal preferences and the specific criteria being considered.",
        "role": "assistant"
      }
    }
  ],
  "created": 1694211759,
  "id": "chatcmpl-7weA3vuMiDI4GhsRrfNN2o4LdpxVe",
  "model": "gpt-3.5-turbo-0613",
  "object": "chat.completion",
  "usage": {
    "completion_tokens": 71,
    "prompt_tokens": 13,
    "total_tokens": 84
  }
}
```

## Orkg examples

The tool can be used to answer questions about the [orkg]() knowledge graph. There are a couple of examples:

### Count number of papers

#### Input:

```sh
python -m spike ask 'How many papers are there'
```

#### Output:

````sh
The SPARQL query to answer the question "How many papers are there?" using the given knowledge graph would be:

```
SELECT (COUNT(?paper) AS ?count)
WHERE {
  ?paper a c:Paper.
}
```

This query selects all instances (`?paper`) that have the type `c:Paper`, and then counts the number of distinct instances using the `COUNT()` function. The result is returned as `?count`.
````

### Count number of research approaches

#### Input:

```sh
python -m spike ask 'How many research approaches are there'
```

#### Output:

````sh
The SPARQL query to answer the question "How many research approaches are there" using the given graph would be:

```
PREFIX r: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX c: <http://orkg.org/orkg/class/>
SELECT (COUNT(?researchApproach) AS ?countResearchApproaches) WHERE {
  ?researchApproach r:type c:C65001 .
}
```

This query selects all instances (`?researchApproach`) that have the type `c:C65001` (which represents the "Research approach" class) and counts the number of occurrences using the `COUNT` function. The result is assigned to the variable `?countResearchApproaches`.
````
