import carto2gpd
import geopandas as gpd
import pandas as pd
from . import EPSG
from .core import Dataset, geocode, replace_missing_geometries
from .regions import *

__all__ = [
    "CrimeIncidents",
    "Shootings",
    "ParkingViolations",
    "StreetCodeViolations",
    "LIViolations", 
    "LIrequests",
]


class CrimeIncidents(Dataset):
    """
    Crime Incidents
    Available: 2006-Present, Updated Daily 
    Selected: 2018 
    
    Source
    ------
    https://www.opendataphilly.org/dataset/crime-incidents
    """

    date_columns = ["dispatch_date_time"]

    @classmethod
    def download(cls, **kwargs):

        # the raw data
        fields = [
            "dc_dist",
            "dc_key",
            "dispatch_date_time",
            "location_block",
            "psa",
            "text_general_code",
            "ucr_general",
        ]
        
        url = "https://phl.carto.com/api/v2/sql"
        where = "extract(year from dispatch_date_time) = 2018"
        gdf = carto2gpd.get(url, "incidents_part1_part2", fields=fields, where=where)

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
    City-wide shooting victims, including Police Officer-involved shootings.
    Available: 2015-yesterday, Updated Daily
    Selected: 2018 

    Source
    ------
    https://www.opendataphilly.org/dataset/shooting-victims
    """

    date_columns = ["date"]

    @classmethod
    def download(cls, **kwargs):

        url = "https://phl.carto.com/api/v2/sql"
        where = "year = 2018"
        gdf = carto2gpd.get(url, "shootings", where=where)

        return (
            replace_missing_geometries(gdf)
            .fillna(np.nan)
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


class ParkingViolations(Dataset):
    """
    Parking Violations
    Available: 2012-2017
    Selected: 2017

    Source
    ------
    https://www.opendataphilly.org/dataset/parking-violations
    """

    date_columns = ["issue_datetime"]

    @classmethod
    def download(cls, **kwargs):
        url = "https://phl.carto.com/api/v2/sql"
        where = "extract(year from issue_datetime) = 2017"
        gdf = carto2gpd.get(url, "parking_violations", where=where)

        return (
            replace_missing_geometries(gdf)
            .to_crs(epsg=EPSG)
            .pipe(geocode, ZIPCodes.get())
            .pipe(geocode, Neighborhoods.get())
            .pipe(geocode, PUMAs.get())
            .assign(
                issue_datetime=lambda df: pd.to_datetime(df.issue_datetime),
                year=lambda df: df.issue_datetime.dt.year,
            )
            .sort_values("issue_datetime", ascending=False)
            .reset_index(drop=True)
        )


class StreetCodeViolations(Dataset):
    """
    Code Violation Notices issued from the Street's department
    Available: 07-21-2009 - 12-27-2048???
    Selected: 2017

    Source
    ------
    https://www.opendataphilly.org/dataset/code-violation-notices
    """

    date_columns = ["date_added"]

    @classmethod
    def download(cls, **kwargs):
        url = "https://phl.carto.com/api/v2/sql"
        where = "extract(year from date_added) = 2017"
        gdf = carto2gpd.get(url, "streets_code_violation_notices", where=where)

        return (
            replace_missing_geometries(gdf)
            .to_crs(epsg=EPSG)
            .pipe(geocode, ZIPCodes.get())
            .pipe(geocode, Neighborhoods.get())
            .pipe(geocode, PUMAs.get())
            .assign(
                date_added=lambda df: pd.to_datetime(df.date_added),
                year=lambda df: df.date_added.dt.year,
            )
            .sort_values("date_added", ascending=False)
            .reset_index(drop=True)
        )


class LIViolations(Dataset):
    """
    Violations issued by the Department of Licenses and Inspections 
    in reference to the Philadelphia Building Construction and OccupancyCode
    Available: 2007-present, Updated Daily 
    Selected: 2018
    
    Source
    ------
    https://www.opendataphilly.org/dataset/licenses-and-inspections-violations
    """
    date_columns = ["violationdate"]

    @classmethod
    def download(cls, **kwargs):
        url = "https://phl.carto.com/api/v2/sql"
        where = "extract(year from violationdate) = 2018"
        gdf = carto2gpd.get(url, "li_violations", where=where)

        return (
            replace_missing_geometries(gdf)
            .to_crs(epsg=EPSG)
            .pipe(geocode, ZIPCodes.get())
            .pipe(geocode, Neighborhoods.get())
            .pipe(geocode, PUMAs.get())
            .assign(
                violationdate=lambda df: pd.to_datetime(df.violationdate),
                year=lambda df: df.violationdate.dt.year,
            )
            .sort_values("violationdate", ascending=False)
            .reset_index(drop=True)
        )


    
    
class LIrequests(Dataset):
    """
    Service requests that were entered via 311 
    Available: 2007-present, Updated Daily 
    Selected: 2018 
    
    Source
    ------
    https://www.opendataphilly.org/dataset/licenses-and-inspections-violations
    """
    
    date_columns = ["sr_calldate"]

    @classmethod
    def download(cls, **kwargs):
        url = "https://phl.carto.com/api/v2/sql"
        where = "extract(year from sr_calldate) = 2018"
        gdf = carto2gpd.get(url, "li_serv_req", where=where)

        return (
            replace_missing_geometries(gdf)
            .to_crs(epsg=EPSG)
            .pipe(geocode, ZIPCodes.get())
            .pipe(geocode, Neighborhoods.get())
            .pipe(geocode, PUMAs.get())
            .assign(
                sr_calldate =lambda df: pd.to_datetime(df.sr_calldate),
                year=lambda df: df.sr_calldate.dt.year,
            )
            .sort_values("sr_calldate", ascending=False)
            .reset_index(drop=True)
        )


    

    
   