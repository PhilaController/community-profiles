import carto2gpd
import pandas as pd
from . import EPSG, DEFAULT_YEAR
from .core import *
from .regions import *


__all__ = ["NewConstructionPermits"]


class NewConstructionPermits(DatasetWithYear):
    """
    New construction building permits.

    Notes
    -----
    Available: 2007 to present
    Update frequency: daily 
    
    Source
    ------
    https://www.opendataphilly.org/dataset/licenses-and-inspections-building-permits
    """

    date_columns = ["permitissuedate"]

    @classmethod
    def download(cls, year=DEFAULT_YEAR):

        # Query CARTO
        gdf = carto2gpd.get(
            "https://phl.carto.com/api/v2/sql",
            "li_permits",
            where=f"extract(year from permitissuedate) = {year} and permitdescription = 'NEW CONSTRUCTION PERMIT'",
        )

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

