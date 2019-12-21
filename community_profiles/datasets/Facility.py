import esri2gpd
import geopandas as gpd
from . import EPSG
from .core import Dataset, geocode, replace_missing_geometries
from .regions import *


__all__ = ["CityOwned", "Parks", "Hospitals", "HealthCenters"]


class CityOwned(Dataset):
    """
    An inventory of buildings and other fixed assets owned, leased, 
    or operated by the City of Philadelphia including buildings, structures, and properties.

    Source
    ------
    http://data.phl.opendata.arcgis.com/datasets/b3c133c3b15d4c96bcd4d5cc09f19f4e_0.zip
    """

    @classmethod
    def download(cls, **kwargs):

        url = "http://data.phl.opendata.arcgis.com/datasets/b3c133c3b15d4c96bcd4d5cc09f19f4e_0.zip"
        df = gpd.read_file(url)

        return (
            df.to_crs(epsg=EPSG)
            .pipe(geocode, ZIPCodes.get())
            .pipe(geocode, Neighborhoods.get())
            .pipe(geocode, PUMAs.get())
        )


class Parks(Dataset):
    """
    Philadephia's Parks & Recreation Assets
    
    Source
    ------
    https://phl.maps.arcgis.com/home/item.html?id=4df9250e3d624ea090718e56a9018694
    """

    @classmethod
    def download(cls, **kwargs):

        fields = ["OBJECTID", "ASSET_NAME", "SITE_NAME", "ADDRESS"]

        url = "https://services.arcgis.com/fLeGjb7u4uXqeF9q/arcgis/rest/services/PPR_Assets/FeatureServer/0"
        gdf = esri2gpd.get(url, fields=fields)

        return (
            gdf.to_crs(epsg=EPSG)
            .pipe(geocode, ZIPCodes.get())
            .pipe(geocode, Neighborhoods.get())
            .pipe(geocode, PUMAs.get())
        )


class Hospitals(Dataset):
    """
    Philadephia's hospitals 
    
    Source
    ------
    https://phl.maps.arcgis.com/home/item.html?id=df8dc18412494e5abbb021e2f33057b2
    """

    @classmethod
    def download(cls, **kwargs):

        fields = ["OBJECTID", "HOSPITAL_NAME", "STREET_ADDRESS", "HOSPITAL_TYPE"]

        url = "https://services.arcgis.com/fLeGjb7u4uXqeF9q/arcgis/rest/services/Hospitals/FeatureServer/0"
        gdf = esri2gpd.get(url, fields=fields)

        return (
            gdf.to_crs(epsg=EPSG)
            .pipe(geocode, ZIPCodes.get())
            .pipe(geocode, Neighborhoods.get())
            .pipe(geocode, PUMAs.get())
        )


class HealthCenters(Dataset):
    """
    Federally Qualified Health Centers

    Source
    ------
    http://data.phl.opendata.arcgis.com/datasets/f87c257e1039470a8a472694c2cd2e4f_0.zip
    """

    @classmethod
    def download(cls, **kwargs):

        url = "http://data.phl.opendata.arcgis.com/datasets/f87c257e1039470a8a472694c2cd2e4f_0.zip"
        df = gpd.read_file(url)

        return (
            df.loc[:, ["NAME", "OBJECTID", "FULL_ADDRE", "geometry"]]
            .to_crs(epsg=EPSG)
            .pipe(geocode, ZIPCodes.get())
            .pipe(geocode, Neighborhoods.get())
            .pipe(geocode, PUMAs.get())
        )

