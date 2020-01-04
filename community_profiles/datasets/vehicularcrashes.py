import carto2gpd
import geopandas as gpd
from . import EPSG
from .core import Dataset, geocode, replace_missing_geometries
from .regions import *

__all__ = [
    "VehicularCrashes",
]


class VehicularCrashes(Dataset):
    """
    Crash data for the years 2007-2017 from the Pennsylvania Department of Transportation (Penn DOT). 
    
    Source
    ------
    https://www.opendataphilly.org/dataset/vehicular-crash-data
    """
    
     @classmethod
    def download(cls, **kwargs):

        url = "https://phl.carto.com/api/v2/sql"
        gdf = carto2gpd.get(url, "crash_data_collision_crash_2007_2017")

        return (
           gdf.to_crs(epsg=EPSG) 
            .pipe(geocode, ZIPCodes.get())
            .pipe(geocode, Neighborhoods.get())
            .pipe(geocode, PUMAs.get())
        )    
        