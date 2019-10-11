import carto2gpd
import geopandas as gpd
import pandas as pd
from . import EPSG
from .core import Dataset, geocode, replace_missing_geometries
from .regions import *

__all__ = [
    "three11",
]

class three11(Dataset):
    """
    311 service requets
    Available: December 8th 2014-Present, Updated Daily 
    
    Source
    ------
    https://www.opendataphilly.org/dataset/311-service-and-information-requests
    """

    date_columns = ["requested_datetime"]

    @classmethod
    def download(cls, **kwargs):
        
        url = "https://phl.carto.com/api/v2/sql"
        gdf = carto2gpd.get(url, "public_cases_fc")

        return (
            replace_missing_geometries(gdf)
            .to_crs(epsg=EPSG)
            .pipe(geocode, ZIPCodes.get())
            .pipe(geocode, Neighborhoods.get())
            .pipe(geocode, PUMAs.get())
            .assign(
                requested_datetime=lambda df: pd.to_datetime(df.requested_datetime),
                year=lambda df: df.requested_datetime.dt.year,
            )
            .sort_values("requested_datetime", ascending=False)
            .reset_index(drop=True)
        )
