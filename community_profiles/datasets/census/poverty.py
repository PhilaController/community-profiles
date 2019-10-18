from .core import CensusDataset
import collections


class Poverty(CensusDataset):
    """
    Poverty in terms of 12 month income below povery_level.   
    
    Source
    ------
    American Community Survey
    """
    
    TABLE_NAME = 'B17001'
    RAW_FIELDS = collections.OrderedDict({
        '001': 'universe',
        '002': 'income_past12months_below_poverty_level',
        '031': 'income_past12months_at_or_above_poverty_level'
    })
    
    
    @classmethod
    def process(cls, df):
                return df
