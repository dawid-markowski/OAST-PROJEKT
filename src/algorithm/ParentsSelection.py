import random

from typing                import Callable, Tuple, List, Dict

from solution.individual import Individual

def randomSelection(
    P: List
) -> Tuple[Individual, Individual]:
    parent1 = random.choice(P)
    parent2 = random.choice(P)
    return parent1, parent2


def elisticSelection(
        P: List,
        L: int = 5 #def elisticSelection(P: List, L: int = 5):,na czas testów wariantu $L=5$
) -> Tuple[Individual, Individual]:
    parent1 = P[0]

    # Jeśli L nie jest podane, domyślnie bierzemy resztę populacji (L = N-1)
    if L is None:
        L = len(P) - 1

    # Losujemy drugiego rodzica z L kolejnych chromosomów (od indeksu 1 do L włącznie)
    parent2 = random.choice(P[1: L + 1])
    return parent1, parent2

def truncationSelection(
    P: List,
    L: int = 5
) -> Tuple[Individual, Individual]:
    # Losujemy dokładnie 2 unikalne chromosomy z L pierwszych na liście
    return random.sample(P[:L], 2)
    
def fitnessProportionateSelection(
    P: List
) -> Tuple[Individual, Individual]:

    N = len(P)

    weights = [
        2 * (N - i)
        /
        (N * (N + 1))
        for i in range(N)
    ]

    parent1 = random.choices(
        P,
        weights=weights,
        k=1
    )[0]

    parent2 = random.choices(
        P,
        weights=weights,
        k=1
    )[0]

    return parent1, parent2

class SelectionType:

    def __init__(
        self,
        selection: Callable=randomSelection
    ) -> None:
        self._selectionType = selection

    def setSelection(
        self,
        selection: Callable=randomSelection
    ) -> None:
        self._selectionType = selection

    def selection(
        self, 
        P: List
    ) -> Tuple[Individual, Individual]:
        return self._selectionType(P)


def setSelectionType(
    jsonContent: Dict
) -> None:

    selectionTypeStr = jsonContent["alg_params"]["selection_type"]

    selection = randomSelection
    match selectionTypeStr.lower():

        case "random_selection":
            pass

        case "elistic_selection":
            selection = elisticSelection

        case "trucation_selection":
            selection = truncationSelection
        
        case "fitness_proportionate_selection":
            selection = fitnessProportionateSelection
        
        case _:
            pass

    selectionType.setSelection(selection)

selectionType = SelectionType()