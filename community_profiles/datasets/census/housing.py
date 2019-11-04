from .core import CensusDataset
import collections

__all__ = ["HousingValue", "MedianHousingValue", "MedianGrossRent", "Tenure"]


class HousingValue(CensusDataset):
    """
    Housing value.
    """

    UNIVERSE = "owner-occupied housing units"
    TABLE_NAME = "B25075"
    RAW_FIELDS = collections.OrderedDict(
        {
            "001": "universe",
            "002": "0_10000",
            "003": "10000_14999",
            "004": "15000_19999",
            "005": "20000_24999",
            "006": "25000_29999",
            "007": "30000_34999",
            "008": "35000_39999",
            "009": "40000_49999",
            "010": "50000_59999",
            "011": "60000_69999",
            "012": "70000_79999",
            "013": "80000_89999",
            "014": "90000_99999",
            "015": "100000_124999",
            "016": "125000_149999",
            "017": "150000_174999",
            "018": "175000_199999",
            "019": "200000_249999",
            "020": "250000_299999",
            "021": "300000_399999",
            "022": "400000_499999",
            "023": "500000_749999",
            "024": "750000_999999",
            "025": "1000000_1499999",
            "026": "1500000_1999999",
            "027": "2000000_more",
        }
    )


class MedianHousingValue(CensusDataset):
    """
    Median housing value.
    """

    UNIVERSE = "owner-occupied housing units"
    TABLE_NAME = "B25077"
    RAW_FIELDS = {"001": "median"}


class MedianGrossRent(CensusDataset):
    """
    Median gross rent (dollars).
    """

    UNIVERSE = "renter-occupied housing units paying cash rent"
    TABLE_NAME = "B25064"
    RAW_FIELDS = {"001": "median"}


class Tenure(CensusDataset):
    """
    Occupied housing units. Owner or renter.
    """

    UNIVERSE = "occupied housing units"
    TABLE_NAME = "B25003"
    RAW_FIELDS = collections.OrderedDict(
        {"001": "universe", "002": "owner_occupied", "003": "renter_occupied"}
    )

