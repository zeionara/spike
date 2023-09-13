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

### Find the best model

#### Input:

```sh
python -m spike ask 'Which model has achieved the highest Accuracy score on the Story Cloze Test benchmark dataset?'
```

#### Message:

````sh
I have a knowledge graph which includes the following fragment:

'
@prefix w: <http://www.w3.org/2002/07/owl#>
@prefix c: <http://orkg.org/orkg/class/>
@prefix p: <http://orkg.org/orkg/predicate#>
@prefix r: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>

c:BENCHMARK_DATASET r:label Benchmark Dataset. _ r:type c:BENCHMARK_DATASET.
c:Benchmark r:label Benchmark. _ r:type c:Benchmark.
c:C14022 r:label Benchmark. _ r:type c:C14022.
c:C14025 r:label Dataset. _ r:type c:C14025.
c:C20019 r:label Data. _ r:type c:C20019.
c:C21025 r:label model. _ r:type c:C21025.
c:C37004 r:label Dataset. _ r:type c:C37004.
c:C58020 r:label Data. _ r:type c:C58020.
c:C58028 r:label Model. _ r:type c:C58028.
c:Data r:label Data. _ r:type c:Data.
c:Dataset r:label Dataset. _ r:type c:Dataset.
c:Model r:label Model. _ r:type c:Model.
p:P2005 r:label dataset. _ p:P2005 _.
p:P18019 r:label Test. _ p:P18019 _.
p:P57032 r:label Highest. _ p:P57032 _.
p:PWC_HAS_BENCHMARK r:label Benchmark. _ p:PWC_HAS_BENCHMARK _.
p:P18048 r:label Accuracy. _ p:P18048 _.
p:P5083 r:label mode. _ p:P5083 _.
p:P1004 r:label model. _ p:P1004 _.
p:P23050 r:label achieved. _ p:P23050 _.
p:DATA r:label Data. _ p:DATA _.
p:P82004 r:label score. _ p:P82004 _.
p:P25052 r:label achieve. _ p:P25052 _.
p:P96045 r:label Dataset. _ p:P96045 _.
'

Generate SPARQL query which allows to answer the question "Which model has achieved the highest Accuracy score on the Story Cloze Test benchmark dataset?" using this graph

Also I know that for a similar question "Which model has achieved the highest Matched score on the MultiNLI benchmark dataset?" the correct query is 
```
SELECT DISTINCT ?model ?model_lbl
WHERE {
  ?metric     a       orkgc:Metric;
              rdfs:label  ?metric_lbl.
  FILTER (str(?metric_lbl) = "Matched")
  {
    SELECT ?model ?model_lbl
    WHERE {
      ?dataset       a                orkgc:Dataset;
                      rdfs:label       ?dataset_lbl.
      FILTER (str(?dataset_lbl) = "MultiNLI")
      ?benchmark      orkgp:HAS_DATASET       ?dataset;
                      orkgp:HAS_EVALUATION    ?eval.
      ?eval           orkgp:HAS_VALUE         ?value;
                      orkgp:HAS_METRIC         ?metric.
      ?cont         orkgp:HAS_BENCHMARK      ?benchmark;
                    orkgp:HAS_MODEL          ?model.
      ?model      rdfs:label               ?model_lbl.
    }
    ORDER BY DESC(?value)
    LIMIT 1
  }
}
```.
Also I know that for a similar question "Which model has achieved the highest Top 5 Accuracy score on the ObjectNet benchmark dataset?" the correct query is 
```
SELECT DISTINCT ?model ?model_lbl
WHERE {
  ?metric     a       orkgc:Metric;
              rdfs:label  ?metric_lbl.
  FILTER (str(?metric_lbl) = "Top 5 Accuracy")
  {
    SELECT ?model ?model_lbl
    WHERE {
      ?dataset       a                orkgc:Dataset;
                      rdfs:label       ?dataset_lbl.
      FILTER (str(?dataset_lbl) = "ObjectNet")
      ?benchmark      orkgp:HAS_DATASET       ?dataset;
                      orkgp:HAS_EVALUATION    ?eval.
      ?eval           orkgp:HAS_VALUE         ?value;
                      orkgp:HAS_METRIC         ?metric.
      ?cont         orkgp:HAS_BENCHMARK      ?benchmark;
                    orkgp:HAS_MODEL          ?model.
      ?model      rdfs:label               ?model_lbl.
    }
    ORDER BY DESC(?value)
    LIMIT 1
  }
}
```.
Also I know that for a similar question "Which model has achieved the highest Score score on the Atari 2600 Berzerk benchmark dataset?" the correct query is 
```
SELECT DISTINCT ?model ?model_lbl
WHERE {
  ?metric     a       orkgc:Metric;
              rdfs:label  ?metric_lbl.
  FILTER (str(?metric_lbl) = "Score")
  {
    SELECT ?model ?model_lbl
    WHERE {
      ?dataset       a                orkgc:Dataset;
                      rdfs:label       ?dataset_lbl.
      FILTER (str(?dataset_lbl) = "Atari 2600 Berzerk")
      ?benchmark      orkgp:HAS_DATASET       ?dataset;
                      orkgp:HAS_EVALUATION    ?eval.
      ?eval           orkgp:HAS_VALUE         ?value;
                      orkgp:HAS_METRIC         ?metric.
      ?cont         orkgp:HAS_BENCHMARK      ?benchmark;
                    orkgp:HAS_MODEL          ?model.
      ?model      rdfs:label               ?model_lbl.
    }
    ORDER BY DESC(?value)
    LIMIT 1
  }
}
```.
````

#### Output

````sh
To answer the question "Which model has achieved the highest Accuracy score on the Story Cloze Test benchmark dataset?", the following SPARQL query can be used:

```
SELECT DISTINCT ?model ?model_lbl
WHERE {
  ?metric     a       orkgc:Metric;
              rdfs:label  ?metric_lbl.
  FILTER (str(?metric_lbl) = "Accuracy")
  {
    SELECT ?model ?model_lbl
    WHERE {
      ?dataset       a                orkgc:Dataset;
                      rdfs:label       ?dataset_lbl.
      FILTER (str(?dataset_lbl) = "Story Cloze Test")
      ?benchmark      orkgp:HAS_DATASET       ?dataset;
                      orkgp:HAS_EVALUATION    ?eval.
      ?eval           orkgp:HAS_VALUE         ?value;
                      orkgp:HAS_METRIC         ?metric.
      ?cont         orkgp:HAS_BENCHMARK      ?benchmark;
                    orkgp:HAS_MODEL          ?model.
      ?model      rdfs:label               ?model_lbl.
    }
    ORDER BY DESC(?value)
    LIMIT 1
  }
}
```

This query will retrieve the model and its label that has achieved the highest Accuracy score on the Story Cloze Test benchmark dataset.
````
