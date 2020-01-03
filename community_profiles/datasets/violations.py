import carto2gpd
import pandas as pd
from . import EPSG, DEFAULT_YEAR
from .core import *
from .regions import *

__all__ = ["ParkingViolations", "StreetCodeViolations", "LIViolations", "LIRequests"]


class ParkingViolations(DatasetWithYear):
    """
    Parking Violations

    Notes
    -----
    Available: 2012-2017
    Selected: 2017

    Source
    ------
    https://www.opendataphilly.org/dataset/parking-violations
    """

    date_columns = ["issue_datetime"]

    @classmethod
    def download(cls, year=2017):

        # Query CARTO
        gdf = carto2gpd.get(
            "https://phl.carto.com/api/v2/sql",
            "parking_violations",
            where=f"extract(year from issue_datetime) = {year}",
        )

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


class StreetCodeViolations(DatasetWithYear):
    """
    A code violation notice is issued from the Street's department when a person
    has violated one or more codes in the City of Philadelphia or violated one
    or more Streets Department rules and regulations. A code violation notice
    (CVN) is a penalty punishable by a fine up to $300.00.

    Notes
    -----
    Available: July 1, 2019 - present
    Update frequency: daily

    Source
    ------
    https://www.opendataphilly.org/dataset/code-violation-notices
    """

    date_columns = ["date_added"]

    @classmethod
    def download(cls, year=DEFAULT_YEAR):

        # Query CARTO
        gdf = carto2gpd.get(
            "https://phl.carto.com/api/v2/sql",
            "streets_code_violation_notices",
            where=f"extract(year from date_added) = {year}",
        )

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


class LIViolations(DatasetWithYear):
    """
    Violations issued by the Department of Licenses and Inspections in reference
    to the Philadelphia Building Construction and Occupancy Code.

    Notes
    -----
    Available: 2007 - present
    Update frequency: daily

    Source
    ------
    https://www.opendataphilly.org/dataset/licenses-and-inspections-violations
    """

    date_columns = ["violationdate"]

    @classmethod
    def download(cls, year=DEFAULT_YEAR):

        # query CARTO
        gdf = carto2gpd.get(
            "https://phl.carto.com/api/v2/sql",
            "li_violations",
            where=f"extract(year from violationdate) = {year}",
        )

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


class LIRequests(Dataset):
    """
    Service requests that were entered via 311 or by an individual in the
    department including a description of the request/complaint, the
    priority/type of the complaint, date of scheduled inspection, who the
    assigned inspector is, and what the outcome of the inspection was, if a case
    or if a case is not required, as well as information about the source of the
    request. 

    Notes
    -----
    Available: 2007-present
    Update frequency: daily 

    Source
    ------
    https://www.opendataphilly.org/dataset/licenses-and-inspections-service-requests
    """

    date_columns = ["sr_calldate"]

    @classmethod
    def download(cls, **kwargs):

        # Query CARTO
        gdf = carto2gpd.get(
            "https://phl.carto.com/api/v2/sql",
            "li_serv_req",
            where=f"extract(year from sr_calldate) = {year}",
        )

        return (
            replace_missing_geometries(gdf)
            .to_crs(epsg=EPSG)
            .pipe(geocode, ZIPCodes.get())
            .pipe(geocode, Neighborhoods.get())
            .pipe(geocode, PUMAs.get())
            .assign(
                sr_calldate=lambda df: pd.to_datetime(df.sr_calldate),
                year=lambda df: df.sr_calldate.dt.year,
            )
            .sort_values("sr_calldate", ascending=False)
            .reset_index(drop=True)
        )

