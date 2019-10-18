from .core import CensusDataset
import collections


class RentBurden(CensusDataset):
    """
    Gross rent as a percentage of household income in the past 12 months.

    Source
    ------
    American Community Survey
    """

    TABLE_NAME = "B25070"
    RAW_FIELDS = collections.OrderedDict(
        {
            "001": "universe",
            "002": "less_than_10",
            "003": "10_to_15",
            "004": "15_to_20",
            "005": "20_to_25",
            "006": "25_to_30",
            "007": "30_to_35",
            "008": "35_to_40",
            "009": "40_to_50",
            "010": "more_than_50",
        }
    )

    @classmethod
    def process(cls, df):

        # More than 35% is defined as rent burdened
        cols = ["35_to_40", "40_to_50", "more_than_50"]
        df["more_than_35"] = df[cols].sum(axis=1)
        df["percent_more_than_35"] = df["more_than_35"] / df["universe"]

        return df

