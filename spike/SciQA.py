from dataclasses import dataclass
from urllib.request import urlretrieve
from zipfile import ZipFile
from os import path
from .util import read_json

URL = 'https://zenodo.org/record/7744048/files/SciQA-dataset.zip'
ARCHIVE_PATH = path.join('assets', 'sciqa.zip')

DATA_PATH_PARENT = 'assets'
DATA_PATH = path.join('assets', 'SciQA-dataset')


@dataclass
class Entry:
    utterance: str
    query: str


class Subset:
    def __init__(self, path: str):
        self.entries = [
            Entry(
                utterance = item['question']['string'],
                query = item['query']['sparql']
            )
            for item in read_json(path)['questions']
        ]

    @property
    def utterances(self):
        return [
            entry.utterance
            for entry in self.entries
        ]


class SciQA:
    def __init__(self):
        if not path.isdir(DATA_PATH):
            if not path.isfile(ARCHIVE_PATH):
                print('Downloading SciQA dataset...')
                urlretrieve(URL, ARCHIVE_PATH)

            print('Extracting SciQA dataset...')
            with ZipFile(ARCHIVE_PATH, 'r') as file:
                file.extractall(DATA_PATH_PARENT)

    @property
    def train(self):
        return Subset(path.join(DATA_PATH, 'train', 'questions.json'))

    @property
    def test(self):
        return Subset(path.join(DATA_PATH, 'test', 'questions.json'))

    @property
    def valid(self):
        return Subset(path.join(DATA_PATH, 'valid', 'questions.json'))
