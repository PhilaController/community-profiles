from .core import CensusDataset
import collections

__all__ = ["PerCapitaIncome"]


class PerCapitaIncome(CensusDataset):
    """
    Per capita income in the past 12 months (in inflation-adjusted dollars).
    """

    UNIVERSE = "total population"
    TABLE_NAME = "B19301"
    RAW_FIELDS = collections.OrderedDict({"001": "per_capita_income"})
