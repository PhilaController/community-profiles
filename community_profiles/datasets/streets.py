import esri2gpd
import geopandas as gpd
from . import EPSG
from .core import Dataset, geocode, replace_missing_geometries
from .regions import *


__all__ = [
    "StreetCondition", 
    "LitterIndex",
]



class StreetCondition(Dataset):
    """
    Street Defect Rating
    
    Source
    ------
    http://phl.maps.arcgis.com/home/item.html?id=288d67ea531c4e1a96ebe43a78b97ca8
    """

    @classmethod
    def download(cls, **kwargs):

        url = "https://services.arcgis.com/fLeGjb7u4uXqeF9q/arcgis/rest/services/Street_Defect_Rating/FeatureServer/0"
        gdf = esri2gpd.get(url)
        
        return ( 
             gdf.to_crs(epsg=EPSG)
            .pipe(geocode, ZIPCodes.get())
            .pipe(geocode, Neighborhoods.get())
            .pipe(geocode, PUMAs.get())
        )
    


class LitterIndex(Dataset):
    """
    Litter Index scores calculated for each street hundred-block.
    2017-2018

    Source
    ------
    http://data-phl.opendata.arcgis.com/datasets/04fa63e09b284dbfbde1983eab367319_0.zip
    """

    @classmethod
    def download(cls, **kwargs):
        
    

        url = "http://data-phl.opendata.arcgis.com/datasets/04fa63e09b284dbfbde1983eab367319_0.zip"
        df = gpd.read_file(url)

        return (
            df.rename(columns={ 'HUNDRED_BL' : 'score'}) 
            .to_crs(epsg=EPSG) 
            .pipe(geocode, ZIPCodes.get())
            .pipe(geocode, Neighborhoods.get())
            .pipe(geocode, PUMAs.get())
        )
 

    