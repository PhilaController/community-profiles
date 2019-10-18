from .core import CensusDataset


class MedianIncome(CensusDataset):
    """
    Median household income.
    """

    TABLE_NAME = 'B19013'
    RAW_FIELDS = {"001": "median"  }
   
    @classmethod
    def process(cls, df):
    
        return df