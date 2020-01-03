import esri2gpd
import geopandas as gpd
from . import EPSG
from .core import Dataset, geocode, replace_missing_geometries
from .regions import *


__all__ = [
    "FoodRetail", 
]


class FoodRetail(Dataset):
    """
    This dataset is derived from the Neighborhood Food Retail in Philadelphia report. 
    
    Looks at neighborhood availability of "high-produce supply stores” (e.g., supermarkets, produce stores, farmers’ markets) 
    in relation to “low-produce supply stores” (like dollar stores, pharmacies, and convenience stores).
    
    Source
    ------
    https://www.opendataphilly.org/dataset/neighborhood-food-retail
    """

    @classmethod
    def download(cls, **kwargs):

       
        url = "https://services.arcgis.com/fLeGjb7u4uXqeF9q/arcgis/rest/services/NeighborhoodFoodRetail/FeatureServer/0"
        gdf = esri2gpd.get(url)

        return ( 
             gdf.to_crs(epsg=EPSG)
            .pipe(geocode, ZIPCodes.get())
            .pipe(geocode, Neighborhoods.get())
            .pipe(geocode, PUMAs.get())
        )

