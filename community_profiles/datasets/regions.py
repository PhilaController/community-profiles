import esri2gpd
import cenpy as cen
import geopandas as gpd
import os
from . import EPSG
from .core import Dataset, data_dir

__all__ = ["CensusTracts", "Neighborhoods", "ZIPCodes", "CityLimits", "PUMAs"]

DEFAULT_YEAR = 2018


class CensusTracts(Dataset):
    """
    The boundary regions for census tracts in Philadelphia 
    from the 2010 Census.
    """

    @classmethod
    def get_path(cls, year=DEFAULT_YEAR):
        return data_dir / cls.__name__ / str(year)

    @classmethod
    def download(cls, **kwargs):
        """
        Download the census tract boundaries
        """
        from phlcensus.regions import CensusTracts

        # Get the year
        year = kwargs.get("year", DEFAULT_YEAR)

        return (
            CensusTracts.get(year=year)[["geometry", "geo_name"]]
            .rename(columns={"geo_name": "census_tract"})
            .to_crs(epsg=EPSG)
        )


class PUMAs(Dataset):
    """
    The boundary regions for the Public Use Microdata Areas (PUMAs) 
    in Philadelphia from the 2010 Census.
    """

    @classmethod
    def get_path(cls, year=DEFAULT_YEAR):
        return data_dir / cls.__name__ / str(year)

    @classmethod
    def download(cls, **kwargs):
        """
        Download the PUMA boundaries
        """
        from phlcensus.regions import PUMAs

        # Get the year
        year = kwargs.get("year", DEFAULT_YEAR)

        return (
            PUMAs.get(year=year)[["geometry", "geo_name"]]
            .rename(columns={"geo_name": "puma"})
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

        from phlcensus.regions import NTAs

        return (
            NTAs.get()[["geometry", "geo_name"]]
            .rename(columns={"geo_name": "neighborhood"})
            .to_crs(epsg=EPSG)
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

        from phlcensus.regions import ZIPCodes

        return ZIPCodes.get().to_crs(epsg=EPSG)
