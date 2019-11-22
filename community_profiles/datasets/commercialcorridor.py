import esri2gpd
import geopandas as gpd
import pandas as pd
from . import EPSG
from .core import Dataset, geocode, replace_missing_geometries
from .regions import *

__all__ = ["CommercialCorridor"]


class CommercialCorridor(Dataset):
    """
    Commercial corridors, centers, districts, and projects that provide consumer-oriented goods and services, 
    including retail, food and beverage, and personal, professional, and business services.
    
    Source
    ------
    https://www.opendataphilly.org/dataset/commercial-corridors
    """

    @classmethod
    def download(cls, **kwargs):
        
        url = "https://services.arcgis.com/fLeGjb7u4uXqeF9q/arcgis/rest/services/Commercial_Corridors/FeatureServer/0"
        gdf = esri2gpd.get(url)
        
        return ( 
             gdf.to_crs(epsg=EPSG)
            .pipe(geocode, ZIPCodes.get())
            .pipe(geocode, Neighborhoods.get())
            .pipe(geocode, PUMAs.get())
        )
                          

