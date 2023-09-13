import json


def read(path: str):
    with open(path, 'r', encoding = 'utf-8') as file:
        return file.read()


def read_json(path: str):
    with open(path, 'r', encoding = 'utf-8') as file:
        return json.load(file)
