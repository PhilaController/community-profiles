from .core import CensusDataset
import collections


class Race(CensusDataset):
    """
    Demographic race data.

    Source
    ------
    American Community Survey
    """

    TABLE_NAME = "B03002"
    RAW_FIELDS = collections.OrderedDict(
        {
            "001": "universe",
            "003": "white_alone",
            "004": "black_alone",
            "005": "american_indian_and_alaska_native",
            "006": "asian_alone",
            "007": "native_hawaiian_and_pacific_islander",
            "008": "other_alone",
            "009": "two_or_more_races",
            "012": "latino_alone",
        }
    )

    @classmethod
    def process(cls, df):

        # add a more general other category
        cols = [
            "american_indian_and_alaska_native",
            "native_hawaiian_and_pacific_islander",
            "other_alone",
            "two_or_more_races",
        ]
        df["all_other_alone"] = df[cols].sum(axis=1)

        return df
