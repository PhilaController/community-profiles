import numpy as np
import pandas as pd
from .core import Dataset
from .regions import *


# load puma data to set indexes
pumas = PUMAs.get().sort_values("geo_id").set_index("geo_id")


def census_count(
    df, group2=None, weight="person_weight", normalize=False, total=None, drop=True
):

    """ Counts the total number of the given data in each PUMA / 
        Calculates percentage of the given data in each PUMA
    
        Parameters
        ----------
        df : DataFrame/GeoDataFrame
        
        group2 : str, optional
            a string keyword that specifies if there is 
            a second column to group by in the groupby function
         
        weight : str, default = 'person_weight'
            change to 'house_weight' for household census data 
        
        normalize : bool, optional
            a boolean keyword that specifies whether to 
            divide by the total to calculate the percentage. 
          
              If normalize = True, need keyword total. 
                
        total : series, optional
            a series to divide the count by to return a percentage.
            
        drop : bool, optional
            a boolean keyword that specifies whether
            to drop the index when resetting 
            
        Returns
        --------
        census_count : series or dataframe 
        
     """

    # Two columns to groupby
    # Returns pivot dataframe with with second group as columns

    if group2 is not None:
        group = df.groupby(["geo_id", group2])
        census_count = group[weight].sum().reset_index()

        census_count = census_count.pivot(
            index="geo_id", columns=group2, values=weight
        ).reset_index(drop=drop)

    # Groupby PUMA
    # Returns series
    else:
        group = df.groupby(["geo_id"])
        census_count = group[weight].sum().reset_index(drop=drop)

    # Divide series or dataframe by total to return percentage
    if normalize:
        census_count = census_count.div(total, axis=0) * 100

    return census_count


def puma_count(df, group2=None, normalize=False, total=None):

    """ Counts the total number of the given data in each PUMA / 
        Calculates percentage of the given data in each PUMA
        
        Parameters
        ----------
        df : DataFrame/GeoDataFrame
        
        group2 : str, optional
            a string keyword that specifies if there is 
            a second column to group by in the groupby function
         
        normalize : bool, optional
            a boolean keyword that specifies whether to divide 
            by the total to calculate the percentage. 
            
                If normalize = True, need keyword total. 
                
        total : series, optional
            a series to divide the count by to return a percentage.
            
        Returns
        --------
        puma_count : series or dataframe 
         
         """

    # Two columns to groupby
    # Returns pivot dataframe with with second group as columns
    if group2 is not None:
        group = df.groupby(["geo_id", group2])
        puma_count = group.size().reset_index()

        puma_count = puma_count.pivot(index="geo_id", columns=group2, values=0).fillna(
            0
        )
    # Groupby PUMA
    # Returns series
    else:
        group = df.groupby(["geo_id"])
        puma_count = group.size().reindex(pumas.index).fillna(0)

    # Divide series or dataframe by total to return percentage
    if normalize:
        puma_count = puma_count.div(total) * 100

    return puma_count

