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
            "01": "universe",
            "02": "0_10000",
            "03": "10000_14999",
            "04": "15000_19999",
            "05": "20000_24999",
            "06": "25000_29999",
            "07": "30000_34999",
            "08": "35000_39999",
            "09": "40000_49999",
            "10": "50000_59999",
            "11": "60000_69999",
            "12": "70000_79999",
            "13": "80000_89999",
            "14": "90000_99999",
            "15": "100000_124999",
            "16": "125000_149999",
            "17": "150000_174999",
            "18": "175000_199999",
            "19": "200000_249999",
            "20": "250000_299999",
            "21": "300000_399999",
            "22": "400000_499999",
            "23": "500000_749999",
            "24": "750000_999999",
            "25": "1000000_1499999",
            "26": "1500000_1999999",
            "27": "2000000_more",
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

