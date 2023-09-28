# Source: https://github.com/emptycrown/llama-hub/blob/00f82de29cdf9c631d872a5c209a3fe9237fd3ab/llama_hub/file/rdf/base.py

"""Read RDF files."""

from pathlib import Path
from typing import Any, Dict, List, Optional

from llama_index.readers.base import BaseReader
from llama_index.readers.schema.base import Document

from tqdm import tqdm


class RDFReader(BaseReader):
    """RDF reader."""

    def __init__(
        self,
        *args: Any,
        **kwargs: Any,
    ) -> None:
        """Initialize loader."""
        super().__init__(*args, **kwargs)

        from rdflib import Graph
        from rdflib.namespace import RDF, RDFS

        self.Graph = Graph
        self.RDF = RDF
        self.RDFS = RDFS

    def fetch_labels(self, uri: Any, graph: Any, lang: str):
        """Fetch all labels of a URI by language."""

        return list(
            filter(
                lambda x: x.language in [lang, None],
                graph.objects(uri, self.RDFS.label),
            )
        )

    def fetch_label_in_graphs(self, uri: Any, lang: str = "en"):
        """Fetch one label of a URI by language from the local or global graph."""

        labels = self.fetch_labels(uri, self.g_local, lang)
        if len(labels) > 0:
            return labels[0].value

        labels = self.fetch_labels(uri, self.g_global, lang)
        if len(labels) > 0:
            return labels[0].value

        inferred_label = str(uri)

        return inferred_label

        # if label.startswith('http'):
        #     components = name[::-1].split('/', maxsplit = 1)
        #
        #     if len(components) > 1:
        #         inferred_label = components[0]

        # raise Exception(f"Label not found for: {uri}")

    def load_data(
        self, file: Path, extra_info: Optional[Dict] = None
    ) -> List[Document]:
        """Parse file."""

        lang = extra_info["lang"] if extra_info is not None else "en"

        self.g_local = self.Graph()
        self.g_local.parse(file)

        self.g_global = self.Graph()
        self.g_global.parse(str(self.RDF))
        self.g_global.parse(str(self.RDFS))

        text_list = []

        n_triples = int(
            list(
                self.g_local.query('select (count(*) as ?cc) where { ?s ?p ?o }')
            )[0][0]
        )

        with tqdm(total = n_triples) as pbar:
            for s, p, o in self.g_local:
                if p == self.RDFS.label:
                    pbar.update()
                    continue
                triple = (
                    f"<{self.fetch_label_in_graphs(s, lang=lang)}> "
                    f"<{self.fetch_label_in_graphs(p, lang=lang)}> "
                    f"<{self.fetch_label_in_graphs(o, lang=lang)}>"
                )
                text_list.append(triple)

                pbar.update()

        text = "\n".join(text_list)

        return [Document(text=text, extra_info=extra_info or {})]
