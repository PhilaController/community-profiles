from .core import CensusDataset
import collections


class EmploymentStatus(CensusDataset):
    """
    Employment status for the population 16 years and older.

    Source
    ------
    American Community Survey
    """

    TABLE_NAME = "B23025"
    RAW_FIELDS = collections.OrderedDict(
        {
            "001": "universe",
            "002": "in_labor_force",
            "003": "civilian",
            "004": "civilian_employed",
            "005": "civilian_unemployed",
            "006": "armed_forces",
            "007": "not_in_labor_force",
        }
    )

    @classmethod
    def process(cls, df):

        # Unemployment rate
        df["unemployment_rate"] = df["civilian_unemployed"] / df["in_labor_force"]

        return df

