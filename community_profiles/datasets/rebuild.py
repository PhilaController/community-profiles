import esri2gpd
import geopandas as gpd
from . import EPSG
from .core import Dataset, geocode, replace_missing_geometries
from .regions import *


class Rebuild(Dataset):
    """
    Philadephia's selected or eligible Rebuild sites.
    The Rebuild program was implemented to improve community facilities. 
    
    Source
    ------
    https://phl.maps.arcgis.com/home/item.html?id=2cee6cd0c0864258b326108707b8942b
    """

    @classmethod
    def download(cls, **kwargs):
        
        fields =  [
            'ASSET_NAME',
            'ASSET_ADDR', 
            'SITE_NAME', 
            'Copy_of_Master_Site_List_9_24_8',
        ]

        url = "https://services.arcgis.com/fLeGjb7u4uXqeF9q/arcgis/rest/services/Rebuild_Sites/FeatureServer/0"
        
        return (
            esri2gpd.get(url, fields = fields)
            .to_crs(epsg=EPSG)
            .rename(columns={'Copy_of_Master_Site_List_9_24_8': 'STATUS'})
            .to_crs(epsg=EPSG)
            .pipe(geocode, ZIPCodes.get())
            .pipe(geocode, Neighborhoods.get())
            .pipe(geocode, PUMAs.get())
                )
