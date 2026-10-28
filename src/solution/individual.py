import random
from typing import List, Dict

from graph.demand import Demand


class Individual:

    def __init__(
        self,
        solutions: Dict[int, List[int]]
    ) -> None:
        self._solutions = solutions

    def getSolutions(self) -> Dict[int, List[int]]:
        return self._solutions


def _generateChromosome(demand: Demand) -> list[int]:
    volume = demand.volume
    maxPaths = demand.maxPaths

    if volume < 0:
        raise ValueError(
            "Wolumen zapotrzebowania nie moze byc ujemny."
        )

    if maxPaths < 1:
        raise ValueError(
            "Zapotrzebowanie musi miec co najmniej jedna sciezke."
        )

    chromosome = []
    remaining = volume

    # Losujemy przepływy dla wszystkich ścieżek oprócz ostatniej.
    for _ in range(maxPaths - 1):
        flow = random.randint(0, remaining)
        chromosome.append(flow)
        remaining -= flow

    # Ostatnia ścieżka otrzymuje cały pozostały ruch.
    chromosome.append(remaining)

    return chromosome


def generateIndividual(
    demands: Dict[int, Demand]
) -> Individual:
    solution = {}

    for demand in demands.values():
        chromosome = _generateChromosome(demand)
        solution[demand.id] = chromosome

    return Individual(solution)