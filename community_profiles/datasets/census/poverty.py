from .core import CensusDataset
import collections

__all__ = ["PovertyStatus"]


class PovertyStatus(CensusDataset):
    """
    Poverty in terms of 12 month income below/above poverty level.
    """

    UNIVERSE = "population for whom poverty status is determined"
    TABLE_NAME = "B17001"
    RAW_FIELDS = collections.OrderedDict(
        {
            "001": "universe",
            "002": "income_past12months_below_poverty_level",
            "031": "income_past12months_at_or_above_poverty_level",
        }
    )

