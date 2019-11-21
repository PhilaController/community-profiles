import carto2gpd
import pandas as pd
import geopandas as gpd
from . import EPSG
from .core import Dataset, geocode, replace_missing_geometries
from .regions import * 


__all__ = ["BusinessLicense"]


class BusinessLicense(Dataset):
    """
    Licenses required by the City to conduct certain business activities.
    Available: 2007 to present
    Selected: 2018 
    
    Source
    ------
    https://www.opendataphilly.org/dataset/licenses-and-inspections-business-licenses
    """

    @classmethod
    def download(cls, **kwargs):

        url = "https://phl.carto.com/api/v2/sql"
        where = "extract(year from initialissuedate) = 2018 and licensestatus = 'Active'"
        gdf = carto2gpd.get(url, "li_business_licenses", where=where)

        return (
        replace_missing_geometries(gdf)
        .to_crs(epsg=EPSG)
        .pipe(geocode, ZIPCodes.get())
        .pipe(geocode, Neighborhoods.get())
        .pipe(geocode, PUMAs.get())
        .assign(
            initialissuedate=lambda df: pd.to_datetime(df.initialissuedate),
            year=lambda df: df.initialissuedate.dt.year,
        )
        .sort_values("initialissuedate", ascending=False)
        .reset_index(drop=True)
    )



