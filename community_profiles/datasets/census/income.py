from .core import CensusDataset


class MedianIncome(CensusDataset):
    """
    Median household income.
    """

    UNIVERSE = "Households"
    TABLE_NAME = "B19013"
    RAW_FIELDS = {"001": "median"}
