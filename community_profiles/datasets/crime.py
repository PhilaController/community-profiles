import carto2gpd
import pandas as pd
import numpy as np
from . import EPSG, DEFAULT_YEAR
from .core import *
from .regions import *

__all__ = ["CrimeIncidents", "Shootings"]


class CrimeIncidents(DatasetWithYear):
    """
    All criminal incidents for the specified year.

    Part 1 & Part 2 Crime Incidents from the Police Department's INCT system
    with generalized UCR codes and addresses rounded to the hundred block. These
    counts may not coincide exactly with data that is submitted to the Uniformed
    Crime Reporting (UCR) system.

    Notes
    -----
    Available: 2006 to present
    Update frequency: daily 

    Source
    ------
    https://www.opendataphilly.org/dataset/crime-incidents
    """

    date_columns = ["dispatch_date_time"]

    @classmethod
    def download(cls, year=DEFAULT_YEAR):

        # Query CARTO
        gdf = carto2gpd.get(
            "https://phl.carto.com/api/v2/sql",
            "incidents_part1_part2",
            fields=[
                "dc_dist",
                "dc_key",
                "dispatch_date_time",
                "location_block",
                "psa",
                "text_general_code",
                "ucr_general",
            ],
            where=f"extract(year from dispatch_date_time) = {year}",
        )

        return (
            replace_missing_geometries(gdf)
            .to_crs(epsg=EPSG)
            .pipe(geocode, ZIPCodes.get())
            .pipe(geocode, Neighborhoods.get())
            .pipe(geocode, PUMAs.get())
            .assign(
                dispatch_date_time=lambda df: pd.to_datetime(df.dispatch_date_time),
                year=lambda df: df.dispatch_date_time.dt.year,
            )
            .sort_values("dispatch_date_time", ascending=False)
            .reset_index(drop=True)
        )


class Shootings(Dataset):
    """
    Citywide shooting victims, including Police Officer-involved shootings.
    
    Notes
    -----
    Available: 2015 to present
    Update frequency: daily

    Source
    ------
    https://www.opendataphilly.org/dataset/shooting-victims
    """

    date_columns = ["date"]

    @classmethod
    def download(cls, year=DEFAULT_YEAR):

        # Query CARTO
        gdf = carto2gpd.get(
            "https://phl.carto.com/api/v2/sql", "shootings", where=f"year = {year}"
        )

        return (
            replace_missing_geometries(gdf)
            .to_crs(epsg=EPSG)
            .pipe(geocode, ZIPCodes.get())
            .pipe(geocode, Neighborhoods.get())
            .pipe(geocode, PUMAs.get())
            .assign(
                time=lambda df: df.time.replace("<Null>", np.nan).fillna("00:00:00"),
                date=lambda df: pd.to_datetime(
                    df.date_.str.slice(0, 10).str.cat(df.time, sep=" ")
                ),
            )
            .drop(labels=["point_x", "point_y", "date_", "time", "objectid"], axis=1)
            .sort_values("date", ascending=False)
            .reset_index(drop=True)
        )

