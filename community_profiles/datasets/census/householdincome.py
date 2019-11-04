from .core import CensusDataset
import collections

__all__ = ["HouseholdIncome"]


class HouseholdIncome(CensusDataset):
    """
    Household income in the past 12 months (in inflation-adjusted dollars).
    """

    UNIVERSE = "households"
    TABLE_NAME = "B19001"
    RAW_FIELDS = collections.OrderedDict(
        {
            "001": "universe",
            "002": "0_9999",
            "003": "10000_14999",
            "004": "15000_19999",
            "005": "20000_24999",
            "006": "25000_29999",
            "007": "30000_34999",
            "008": "35000_39999",
            "009": "40000_44999",
            "010": "45000_49999",
            "011": "50000_59999",
            "012": "60000_74999",
            "013": "75000_99999",
            "014": "100000_124999",
            "015": "125000_149999",
            "016": "150000_199999",
            "017": "200000_more",
        }
    )

