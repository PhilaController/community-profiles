import esri2gpd
import cenpy as cen
import geopandas as gpd
import os
from . import EPSG
from .core import Dataset, data_dir

__all__ = [
    "PlanningDistricts",
    "CensusTracts",
    "Neighborhoods",
    "ZIPCodes",
    "CityLimits",
    "PUMAs",
]


class PlanningDistricts(Dataset):
    """
    Planning districts in the city of Philadelphia
    """

    @classmethod
    def download(cls, **kwargs):

        url = "https://services.arcgis.com/fLeGjb7u4uXqeF9q/arcgis/rest/services/Planning_Districts/FeatureServer/0"
        return esri2gpd.get(url).to_crs(epsg=EPSG)


class CensusTracts(Dataset):
    """
    The boundary regions for census tracts in Philadelphia 
    from the 2010 Census.
    """

    @classmethod
    def get_path(cls, year=2017):
        return data_dir / cls.__name__ / str(year)

    @classmethod
    def download(cls, **kwargs):
        """
        Download the census tract boundaries
        """
        # Get the year
        year = kwargs.get("year", 2017)

        return (
            esri2gpd.get(
                f"http://tigerweb.geo.census.gov/arcgis/rest/services/TIGERweb/tigerWMS_ACS{year}/MapServer/8",
                where="STATE=42 AND COUNTY=101",
                fields=["GEOID", "NAME"],
            )
            .rename(columns={"GEOID": "geo_id", "NAME": "geo_name"})
            .sort_values("geo_id")
            .reset_index(drop=True)
            .to_crs(epsg=EPSG)
        )


class PUMAs(Dataset):
    """
    The boundary regions for the Public Use Microdata Areas (PUMAs) 
    in Philadelphia from the 2010 Census.
    """

    @classmethod
    def get_path(cls, year=2017):
        return data_dir / cls.__name__ / str(year)

    @classmethod
    def download(cls, **kwargs):
        """
        Download the PUMA boundaries
        """
        # Get the year
        year = kwargs.get("year", 2017)

        return (
            esri2gpd.get(
                f"http://tigerweb.geo.census.gov/arcgis/rest/services/TIGERweb/tigerWMS_ACS{year}/MapServer/0",
                where="STATE=42 AND PUMA LIKE '%032%'",
                fields=["GEOID", "NAME"],
            )
            .rename(columns={"GEOID": "geo_id", "NAME": "geo_name"})
            .sort_values("geo_id")
            .reset_index(drop=True)
            .to_crs(epsg=EPSG)
        )


class CityLimits(Dataset):
    """
    Philadelphia's city limits.

    Source
    ------
    http://phl.maps.arcgis.com/home/item.html?id=405ec3da942d4e20869d4e1449a2be48
    """

    @classmethod
    def download(cls, **kwargs):

        url = "https://services.arcgis.com/fLeGjb7u4uXqeF9q/arcgis/rest/services/City_Limits/FeatureServer/0"
        return esri2gpd.get(url).to_crs(epsg=EPSG)


class Neighborhoods(Dataset):
    """
    Polygons representing Philadelphia's neighborhoods.

    Notes
    -----
    These are Zillow-based neighborhoods.

    Source
    ------
    https://phl.maps.arcgis.com/home/item.html?id=ab9d26be1df8486c8d5d706fb32b33d5
    """

    @classmethod
    def download(cls, **kwargs):

        url = "https://services.arcgis.com/fLeGjb7u4uXqeF9q/ArcGIS/rest/services/Philly_Neighborhoods/FeatureServer/0"
        return (
            esri2gpd.get(url, fields=["MAPNAME"])
            .to_crs(epsg=EPSG)
            .rename(columns={"MAPNAME": "neighborhood"})
        )


class ZIPCodes(Dataset):
    """
    Polygons representing Philadelphia's ZIP codes.

    Notes
    -----
    These are from the 2018 Census ZIP Code Tabulation Areas (ZCTAs).

    Source
    ------
    https://phl.maps.arcgis.com/home/item.html?id=ab9d26be1df8486c8d5d706fb32b33d5
    """

    @classmethod
    def download(cls, **kwargs):

        url = "https://services.arcgis.com/fLeGjb7u4uXqeF9q/arcgis/rest/services/Philadelphia_ZCTA_2018/FeatureServer/0"
        return esri2gpd.get(url, fields=["zip_code"]).to_crs(epsg=EPSG)

