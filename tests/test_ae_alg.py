from src.algorithm.ParamsImporter import ParamsImporter


def test_default_params_init() -> None:

    paramsImporter = ParamsImporter()

    assert paramsImporter.getPopulationSize()               == 20
    assert paramsImporter.getCrossovers()                   == 10
    assert paramsImporter.getIndividualMutationProbability() == 0.1
    assert paramsImporter.getGeneMutationProbability()      == 0.1
    assert paramsImporter.getSeed()                         == 13
    assert paramsImporter.getEpochsNum()                    == 1000