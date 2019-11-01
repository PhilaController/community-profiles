from .core import CensusDataset


class MedianHouseValue(CensusDataset):
    """
    Median housing value.
    """

    UNIVERSE = "Owner-occupied housing units"
    TABLE_NAME = "B25077"
    RAW_FIELDS = {"001": "median"}
