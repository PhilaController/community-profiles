from .core import CensusDataset
import collections


class Poverty(CensusDataset):
    """
    Poverty in terms of 12 month income below poverty level.   
    
    Source
    ------
    American Community Survey
    """

    UNIVERSE = "Population for whom poverty status is determined"
    TABLE_NAME = "B17001"
    RAW_FIELDS = collections.OrderedDict(
        {
            "001": "universe",
            "002": "income_past12months_below_poverty_level",
            "031": "income_past12months_at_or_above_poverty_level",
        }
    )

