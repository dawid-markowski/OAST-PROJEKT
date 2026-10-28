import os
import random

from typing import Dict, List, Any

from algorithm.ParamsImporter import ParamsImporter, importAlgParams
from algorithm.solver import solver

from graph.link import Links, openLinkParams
from graph.demand import Demand, openLinkDemands
from graph.DemandPathLink import DemandPath, loadDemandPaths

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DEFAUTL_PATH = os.path.join(BASE_DIR, "params.json")


def _setupProblemPath(
        problemType: str
) -> str:
    if problemType.lower() == "dap":
        return os.path.join(BASE_DIR, "alg_params", "dap-net4-26Z.txt")

    if problemType.lower() == "ddap":
        return os.path.join(BASE_DIR, "alg_params", "ddap-net4-26Z.txt")

    return ""

def main() -> None:

    # import data
    algParams, problemType = importAlgParams(path=DEFAUTL_PATH)
    problemTypePath        = _setupProblemPath(problemType)
    links                  = openLinkParams(path=problemTypePath)
    demands                = openLinkDemands(path=problemTypePath)
    demandPathLink         = loadDemandPaths(path=problemTypePath)

    random.seed(algParams.getSeed())

    solver(
        algParams=algParams,
        links=links,
        demands=demands,
        demandPathLink=demandPathLink,
        problemType=problemType  # (D)DAP
    )
if __name__ == "__main__":
    main()