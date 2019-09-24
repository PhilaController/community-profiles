import esri2gpd
import geopandas as gpd
from . import EPSG
from .core import Dataset


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

        url = "https://services.arcgis.com/fLeGjb7u4uXqeF9q/arcgis/rest/services/Rebuild_Sites/FeatureServer/0"
        return esri2gpd.get(url).to_crs(epsg=EPSG)