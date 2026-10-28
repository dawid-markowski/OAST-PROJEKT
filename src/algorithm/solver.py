import csv
import random
from pathlib import Path
from copy import deepcopy
from collections import defaultdict
from bisect import bisect_right
from typing import Dict

from graph.demand import Demand
from graph.link import Links
from solution.individual import Individual, generateIndividual
from algorithm.ParamsImporter import ParamsImporter


def _evaluate(
    individual: Individual,
    demandPathLink: Dict,
    links: Links,
    problem_type: str
) -> int:
    link_loads = defaultdict(int)

    # Sumowanie ruchu przechodzącego przez każde łącze.
    for demand_id, gene in individual.getSolutions().items():
        for path_id, flow in enumerate(gene, start=1):
            if flow > 0:
                path = demandPathLink[demand_id][path_id]

                for link_id in path.links:
                    link_loads[link_id] += flow

    if problem_type == "DAP":
        # Maksymalne przeciążenie, także gdy jest ujemne.
        return max(
            link_loads[link_id] - link.value * links.moduleCapacity
            for link_id, link in links.getLink().items()
        )

    if problem_type == "DDAP":
        total_cost = 0
        module_capacity = links.moduleCapacity

        for link_id, link in links.getLink().items():
            load = link_loads[link_id]

            # Dzielenie całkowite z zaokrągleniem w górę.
            modules_needed = (
                load + module_capacity - 1
            ) // module_capacity

            total_cost += modules_needed * link.value

        return total_cost

    raise ValueError("Nieznany typ problemu: " + problem_type)


def _crossover(
    parent1: Individual,
    parent2: Individual
):
    genes1 = parent1.getSolutions()
    genes2 = parent2.getSolutions()

    child1_genes = {}
    child2_genes = {}

    # Gen to cały przydział ruchu jednego zapotrzebowania.
    for demand_id in genes1:
        if random.random() < 0.5:
            child1_genes[demand_id] = deepcopy(genes1[demand_id])
            child2_genes[demand_id] = deepcopy(genes2[demand_id])
        else:
            child1_genes[demand_id] = deepcopy(genes2[demand_id])
            child2_genes[demand_id] = deepcopy(genes1[demand_id])

    return Individual(child1_genes), Individual(child2_genes)


def _mutate(
    individual: Individual,
    p: float,
    q: float
) -> None:
    # Pierwszy poziom: czy mutujemy tego osobnika?
    if random.random() >= p:
        return

    # Drugi poziom: osobne losowanie dla każdego genu.
    for gene in individual.getSolutions().values():
        if random.random() >= q:
            continue

        if len(gene) < 2:
            continue

        active_paths = [
            i for i, flow in enumerate(gene)
            if flow > 0
        ]

        if not active_paths:
            continue

        path_from = random.choice(active_paths)

        available_targets = [
            i for i in range(len(gene))
            if i != path_from
        ]

        path_to = random.choice(available_targets)

        # Przenosimy jedną jednostkę, zachowując sumę ruchu.
        gene[path_from] -= 1
        gene[path_to] += 1


def _insert_sorted(
    population: list,
    individual: Individual,
    evaluate
) -> None:
    # Wstawienie osobnika z zachowaniem kolejności ocen.
    score = evaluate(individual)
    scores = [evaluate(item) for item in population]
    position = bisect_right(scores, score)
    population.insert(position, individual)

def _print_result(
    individual: Individual,
    demandPathLink: Dict,
    links: Links,
    problem_type: str
) -> None:
    link_loads = defaultdict(int)

    print("\n--- PRZEPLYWY SCIEZKOWE ---")

    for demand_id, gene in individual.getSolutions().items():
        print(f"Zapotrzebowanie {demand_id}:")

        for path_id, flow in enumerate(gene, start=1):
            path = demandPathLink[demand_id][path_id]

            print(
                f"  Sciezka {path_id}: "
                f"przeplyw={flow}, lacza={path.links}"
            )

            for link_id in path.links:
                link_loads[link_id] += flow

    print("\n--- OBCIAZENIA LACZY ---")

    for link_id, link in links.getLink().items():
        load = link_loads[link_id]

        if problem_type == "DAP":
            capacity = link.value * links.moduleCapacity
            overload = load - capacity

            print(
                f"Lacze {link_id}: "
                f"obciazenie={load}, "
                f"pojemnosc={capacity}, "
                f"przeciazenie={overload}"
            )

        elif problem_type == "DDAP":
            modules = (
                load + links.moduleCapacity - 1
            ) // links.moduleCapacity

            capacity = modules * links.moduleCapacity
            cost = modules * link.value

            print(
                f"Lacze {link_id}: "
                f"obciazenie={load}, "
                f"moduly={modules}, "
                f"pojemnosc={capacity}, "
                f"koszt={cost}"
            )

    objective = _evaluate(
        individual,
        demandPathLink,
        links,
        problem_type
    )

    print(f"\nWartosc funkcji celu ({problem_type}): {objective}")

def _save_trajectory(trajectory, problem_type: str) -> None:
    project_dir = Path(__file__).resolve().parents[2]
    results_dir = project_dir / "results"
    results_dir.mkdir(parents=True, exist_ok=True)

    output_path = results_dir / f"{problem_type.lower()}_trajectory.csv"

    with output_path.open("w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["generation", "best_objective"])
        writer.writerows(trajectory)

    print(f"\nZapisano przebieg do: {output_path}")

def solver(
    algParams: ParamsImporter,
    links: Links,
    demands: Dict[int, Demand],
    demandPathLink: Dict,
    problemType: str
) -> Individual:
    population_size = algParams.getPopulationSize()
    epochs = algParams.getEpochsNum()
    crossovers = algParams.getCrossovers()

    p = algParams.getIndividualMutationProbability()
    q = algParams.getGeneMutationProbability()

    if population_size < 1:
        raise ValueError("Populacja musi zawierać co najmniej 1 osobnika.")

    if crossovers < 0 or epochs < 0:
        raise ValueError("Liczba krzyżowań i generacji nie może być ujemna.")

    if not (0 <= p <= 1 and 0 <= q <= 1):
        raise ValueError("Prawdopodobieństwa p i q muszą należeć do [0, 1].")

    if problemType not in ("DAP", "DDAP"):
        raise ValueError("Typ problemu musi być DAP albo DDAP.")

    if not links.getLink() or links.moduleCapacity <= 0:
        raise ValueError("Sieć musi mieć łącza i dodatnią pojemność modułu.")

    random.seed(algParams.getSeed())

    def evaluate(individual: Individual) -> int:
        return _evaluate(
            individual,
            demandPathLink,
            links,
            problemType
        )

    # Populacja początkowa jest uporządkowana.
    P = []

    for _ in range(population_size):
        individual = generateIndividual(demands)
        _insert_sorted(P, individual, evaluate)

    trajectory = [(0, evaluate(P[0]))]

    print(
        f"Generacja 0 | Najlepszy wynik ({problemType}): "
        f"{evaluate(P[0])}"
    )

    for generation in range(1, epochs + 1):
        O = []

        # Dokładnie K krzyżowań daje dokładnie 2K potomków.
        for _ in range(crossovers):
            parent1 = random.choice(P)
            parent2 = random.choice(P)

            child1, child2 = _crossover(parent1, parent2)

            _insert_sorted(O, child1, evaluate)
            _insert_sorted(O, child2, evaluate)

        # Kopia listy pozwala odwiedzić każdego potomka raz,
        # mimo zmiany kolejności elementów w O.
        for individual in list(O):
            O.remove(individual)

            _mutate(individual, p, q)

            # Po mutacji ocena może się zmienić.
            _insert_sorted(O, individual, evaluate)

        # Wybieramy N najlepszych spośród rodziców i potomków.
        candidates = sorted(P + O, key=evaluate)
        P = candidates[:population_size]

        trajectory.append((generation, evaluate(P[0])))

        print(
            f"Generacja {generation} | "
            f"Najlepszy wynik ({problemType}): {evaluate(P[0])}"
        )

    best = P[0]

    print("\n--- KONIEC ---")
    print(f"Ostateczny najlepszy wynik: {evaluate(best)}")

    _print_result(
        best,
        demandPathLink,
        links,
        problemType
    )

    _save_trajectory(trajectory, problemType)

    return best