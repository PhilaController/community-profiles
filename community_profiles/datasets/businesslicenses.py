import carto2gpd
import pandas as pd
from . import EPSG, DEFAULT_YEAR
from .core import *
from .regions import *


__all__ = ["BusinessLicenses"]


class BusinessLicenses(DatasetWithYear):
    """
    Active business licenses, which are required by the City to conduct 
    certain business activities.

    Licenses are required for individuals and businesses to engage in select 
    commercial activities. For example, vendors and restaurants require a license 
    in order to sell goods and food and trades-people, such as plumbers and 
    contractors, require a license in order to practice their trade.

    Notes
    -----
    Available: 2007 to present
    Update frequency: daily 

    Source
    ------
    https://www.opendataphilly.org/dataset/licenses-and-inspections-business-licenses
    """

    date_columns = ["initialissuedate", "mostrecentissuedate"]

    @classmethod
    def download(cls, year=DEFAULT_YEAR):

        # Query carto for all active licenses from a specific year
        gdf = carto2gpd.get(
            "https://phl.carto.com/api/v2/sql",
            "li_business_licenses",
            where=f"extract(year from initialissuedate) = {year} and licensestatus = 'Active'",
        )

        # Geocode and return
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

