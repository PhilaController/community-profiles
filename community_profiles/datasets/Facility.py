import esri2gpd
import geopandas as gpd
from . import EPSG
from .core import Dataset


__all__ = ["CityOwned", "Schools", "Parks", "Hospitals", "HealthCenters"]


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

        return df.to_crs(epsg=EPSG) 

    
    
class Schools(Dataset):
    """
    Philadephia's schools (all types) 
    
    Source
    ------
    https://phl.maps.arcgis.com/home/item.html?id=d46a7e59e2c246c891fbee778759717e
    """

    @classmethod
    def download(cls, **kwargs):

        url = "https://services.arcgis.com/fLeGjb7u4uXqeF9q/arcgis/rest/services/Schools/FeatureServer/0"
        return esri2gpd.get(url).to_crs(epsg=EPSG)    
    
   

    
class Parks(Dataset):
    """
    Philadephia's Parks & Recreation Assets
    
    Source
    ------
    https://phl.maps.arcgis.com/home/item.html?id=4df9250e3d624ea090718e56a9018694
    """

    @classmethod
    def download(cls, **kwargs):

        url = "https://services.arcgis.com/fLeGjb7u4uXqeF9q/arcgis/rest/services/PPR_Assets/FeatureServer/0"
        return esri2gpd.get(url).to_crs(epsg=EPSG)    
    
    
    
class Hospitals(Dataset):
    """
    Philadephia's hospitals 
    
    Source
    ------
    https://phl.maps.arcgis.com/home/item.html?id=df8dc18412494e5abbb021e2f33057b2
    """

    @classmethod
    def download(cls, **kwargs):

        url = "https://services.arcgis.com/fLeGjb7u4uXqeF9q/arcgis/rest/services/Hospitals/FeatureServer/0"
        return esri2gpd.get(url).to_crs(epsg=EPSG)    
    
    
    
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

        return df.to_crs(epsg=EPSG) 
    
    