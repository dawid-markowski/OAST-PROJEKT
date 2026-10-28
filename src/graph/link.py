import re

from typing import Dict

from .utils import importData


class Link:

    def __init__(
        self,
        nodeA: int,
        nodeZ: int,
        value: int
    ) -> None:
        self.nodeA = nodeA
        self.nodeZ = nodeZ
        # liczba modułów (DAP) albo koszt modułu (DDAP)
        self.value = value

    def __repr__(
        self
    ) -> str:
        return f"Link(nodeA={self.nodeA}, nodeZ={self.nodeZ}, value={self.value})"


class Links:

    def __init__(
        self,
        moduleCapacity: int,
        links: Dict[int, Link]
    ) -> None:
        self.moduleCapacity = moduleCapacity
        self.links = links

    def getLink(
        self
    ) -> Dict[int, Link]:
        return self.links

    def __repr__(
        self
    ) -> str:
        return f"Links(moduleCapacity={self.moduleCapacity}, links={self.links})"


def _importLink(
    content: str
) -> Links:

    capacity_match = re.search(r"param\s+moduleCapacity\s*:=\s*(\d+);", content)
    if capacity_match is None:
        raise ValueError("Brak parametru 'moduleCapacity' w pliku z danymi")
    module_capacity = int(capacity_match.group(1))

    if "param: Links:" not in content:
        raise ValueError("Brak sekcji 'param: Links:' w pliku z danymi")

    section = content.split("param: Links:")[1].split(";")[0]

    if ":=" not in section:
        raise ValueError("Sekcja Links nie zawiera ':='")

    rows = section.split(":=")[1].strip().splitlines()

    links_dict = {}
    for i, row in enumerate(rows):
        if not row.strip():
            continue

        data = list(map(int, row.split()))

        if len(data) != 4:
            raise ValueError(
                f"Links, wiersz {i + 1}: oczekiwano 4 wartości, jest {len(data)}"
            )

        links_dict[data[0]] = Link(data[1], data[2], data[3])

    return Links(module_capacity, links_dict)


def openLinkParams(
    path: str = ""
) -> Links | None:

    data = importData(path=path)

    if data == "":
        return None

    return _importLink(data)
