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
    P: List
) -> Tuple[Individual, Individual]:
    parent1 = P[0]
    parent2 = random.choice(P[1:len(P)+1])
    return parent1, parent2

def trucationSelection(
    P: List
) -> Tuple[Individual, Individual]:
    return random.sample(P[:len(P)], 2)

def fitnessProportionateSelection(
    P: List
) -> Tuple[Individual, Individual]:


    print("P =", P[:3])
    print("Typ pierwszego elementu:", type(P[0]))

    
    scores = [score for score, _ in P]

    # zamiana problemu minimalizacyjnego na wagi
    weights = [
        1.0 / (score + 1e-9)
        for score in scores
    ]

    parent1 = random.choices(
        P,
        weights=weights,
        k=1
    )[0][1]

    parent2 = random.choices(
        P,
        weights=weights,
        k=1
    )[0][1]

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
            selection = trucationSelection
        
        case "fitness_proportionate_selection":
            selection = fitnessProportionateSelection
        
        case _:
            pass

    selectionType.setSelection(selection)

selectionType = SelectionType()