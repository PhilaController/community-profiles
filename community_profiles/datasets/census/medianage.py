from .core import CensusDataset
import collections

__all__ = ["MedianAge"]


class MedianAge(CensusDataset):
    """
    Median age by sex.
    """

    UNIVERSE = "total population"
    TABLE_NAME = "B01002"
    RAW_FIELDS = collections.OrderedDict(
        {"001": "median", "002": "male", "003": "female"}
    )
