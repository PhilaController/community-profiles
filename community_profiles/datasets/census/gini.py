from .core import CensusDataset


class GiniIncomeInequality(CensusDataset):
    """
    Gini index of income inequality for all households.

    Source
    ------
    American Community Survey
    """

    TABLE_NAME = "B19083"
    RAW_FIELDS = {"001": "gini_index"}

