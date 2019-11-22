import carto2gpd
import pandas as pd
import geopandas as gpd
from . import EPSG
from .core import Dataset, geocode, replace_missing_geometries
from .regions import *


__all__ = ["NewConstruction"]



class NewConstruction(Dataset):
    """
    Building and Zoning Permits 
    Available: 2007 to Present, Updated Daily 
    Selected: 2018 
    
    Source
    ------
    https://www.opendataphilly.org/dataset/licenses-and-inspections-building-permits
    """

    @classmethod
    def download(cls, **kwargs):

        url = "https://phl.carto.com/api/v2/sql"
        where = "extract(year from permitissuedate) = 2018 and permitdescription = 'NEW CONSTRUCTION PERMIT'"
        gdf = carto2gpd.get(url, "li_permits", where=where)

        return (
            replace_missing_geometries(gdf)
            .to_crs(epsg=EPSG)
            .pipe(geocode, ZIPCodes.get())
            .pipe(geocode, Neighborhoods.get())
            .pipe(geocode, PUMAs.get())
            .assign(
                permitissuedate=lambda df: pd.to_datetime(df.permitissuedate),
                year=lambda df: df.permitissuedate.dt.year,
            )
            .sort_values("permitissuedate", ascending=False)
            .reset_index(drop=True)
        )

