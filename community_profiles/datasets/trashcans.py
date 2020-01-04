import carto2gpd
import esri2gpd
import geopandas as gpd
from . import EPSG
from .core import Dataset, geocode, replace_missing_geometries
from .regions import *

__all__ = [
    "BigBelly",
    "WireWasteBasket",
]


class BigBelly(Dataset):
    """
    Big Belly brand waste baskets maintained/collected by the City of Philadelphia.
    
    Source
    ------
    https://www.opendataphilly.org/dataset/big-belly-waste-bins
    """
    
    @classmethod
    def download(cls, **kwargs):

        url = "https://phl.carto.com/api/v2/sql"
        gdf = carto2gpd.get(url, "wastebaskets_big_belly")  

        return (
            gdf.to_crs(epsg=EPSG) 
            .pipe(geocode, ZIPCodes.get())
            .pipe(geocode, Neighborhoods.get())
            .pipe(geocode, PUMAs.get())
        )
    
    
    
class WireWasteBasket(Dataset):
    """ 
    Non Big Belly waste baskets maintained/collected by the City of Philadelphia.
    
    Source 
    ------
    https://www.opendataphilly.org/dataset/wire-waste-baskets
    """
    

    @classmethod
    def download(cls, **kwargs):

        url = "https://services.arcgis.com/fLeGjb7u4uXqeF9q/arcgis/rest/services/WasteBaskets_Wire/FeatureServer/0"
        gdf = esri2gpd.get(url)
        
        return ( 
             gdf.to_crs(epsg=EPSG)
            .pipe(geocode, ZIPCodes.get())
            .pipe(geocode, Neighborhoods.get())
            .pipe(geocode, PUMAs.get())
        )
    

    