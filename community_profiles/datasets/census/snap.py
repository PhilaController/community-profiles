from .core import CensusDataset
import collections

__all__ = ["Snap"]


class Snap(CensusDataset):
    """
    Household received Food Stamps/SNAP in the past 12 months
    """

    UNIVERSE = "household"
    TABLE_NAME = "B22003"
    RAW_FIELDS = collections.OrderedDict(
        {
            "001": "universe",
            "002": "recipient",
            "05": "nonrecipient",
        }
    )