import carto2gpd
import geopandas as gpd
import pandas as pd
from . import EPSG, DEFAULT_YEAR
from .core import *
from .regions import *

__all__ = ["ServiceRequests311"]


class ServiceRequests311(DatasetWithYear):
    """
    311 service requests

    Notes
    -----
    Available: 2015 to Present
    Update frequency: daily 
    
    Source
    ------
    https://www.opendataphilly.org/dataset/311-service-and-information-requests
    """

    date_columns = ["requested_datetime"]

    @classmethod
    def download(cls, year=DEFAULT_YEAR):

        url = "https://phl.carto.com/api/v2/sql"
        gdf = carto2gpd.get(
            url,
            "public_cases_fc",
            where=f"extract(year from requested_datetime) = {year}",
        )

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
