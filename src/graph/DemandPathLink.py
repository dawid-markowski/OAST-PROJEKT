import  re
from    typing import Dict, List
from    .utils import importData


class DemandPath:

    def __init__(
        self,
        demand_id:  int,
        path_id:    int,
        links:      List[int]
    ) -> None:
        self.demand_id = demand_id
        self.path_id   = path_id
        self.links     = links

    def __repr__(
        self
    ) -> str:
        return (
            f"DemandPath(demand_id={self.demand_id}, "
            f"path_id={self.path_id}, links={self.links})"
        )


_PATTERN = re.compile(
    r"set\s+Demand(?:Path_links|_pathLinks)\[(\d+),(\d+)\]\s*:=\s*([\d\s]+);"
)


def _importDemandPaths(
    content: str
) -> Dict[int, Dict[int, DemandPath]]:

    demand_paths: Dict[int, Dict[int, DemandPath]] = {}

    for line in content.splitlines():
        match = _PATTERN.search(line)

        if match is None:
            continue

        demand_id = int(match.group(1))
        path_id   = int(match.group(2))
        links     = [int(x) for x in match.group(3).split()]

        demand_paths.setdefault(demand_id, {})[path_id] = DemandPath(
            demand_id,
            path_id,
            links
        )

    if not demand_paths:
        raise ValueError("Nie znaleziono żadnych ścieżek (DemandPath_links / Demand_pathLinks)")

    return demand_paths


def loadDemandPaths(
    path: str
) -> Dict[int, Dict[int, DemandPath]] | None:

    data = importData(path=path)

    if data == "":
        return None

    return _importDemandPaths(data)
