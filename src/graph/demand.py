from    typing import Dict

from    .utils import importData


class Demand:

    def __init__(
        self,
        demand_id: int,
        src:       int,
        dst:       int,
        volume:    int,
        maxPaths:  int
    ) -> None:
        self.id        = demand_id
        self.src       = src
        self.dst       = dst
        self.volume    = volume
        self.maxPaths  = maxPaths

    def __repr__(
        self
    ) -> str:
        return (
            f"Demand(id={self.id}, src={self.src}, dst={self.dst}, "
            f"volume={self.volume}, maxPaths={self.maxPaths})"
        )


def _importDemands(
    content: str
) -> Dict[int, Demand]:

    if "param: Demands:" not in content:
        raise ValueError("Brak sekcji 'param: Demands:' w pliku z danymi")

    section = content.split("param: Demands:")[1].split(";")[0]

    if ":=" not in section:
        raise ValueError("Sekcja Demands nie zawiera ':='")

    rows    = section.split(":=")[1].strip().splitlines()
    demands = {}

    for i, row in enumerate(rows):
        if not row.strip():
            continue

        data = list(map(int, row.split()))

        if len(data) != 5:
            raise ValueError(
                f"Demands, wiersz {i + 1}: oczekiwano 5 wartości, jest {len(data)}"
            )

        demands[i] = Demand(
            data[0],
            data[1],
            data[2],
            data[3],
            data[4]
        )

    return demands


def openLinkDemands(
    path: str = ""
) -> Dict[int, Demand] | None:

    data = importData(path=path)

    if data == "":
        return None

    return _importDemands(data)
