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
