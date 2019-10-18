from .core import CensusDataset


class MedianHouseValue(CensusDataset):
    """
    Median houseing value.
    """

    TABLE_NAME = 'B25077'
    RAW_FIELDS = { "001": "median"}

    
    @classmethod
    def process(cls, df):
    
        return df