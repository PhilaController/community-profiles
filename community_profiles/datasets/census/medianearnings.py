from .core import CensusDataset
import collections

__all__ = ["MedianEarnings"]


class MedianEarnings(CensusDataset):
    """
    Median earnings by sex.
    """

    UNIVERSE = "population 16 years and over with earnings"
    TABLE_NAME = "B20002"
    RAW_FIELDS = collections.OrderedDict(
        {"001": "total", "002": "male", "003": "female"}
    )

