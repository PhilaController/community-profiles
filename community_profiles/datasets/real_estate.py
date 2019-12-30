import carto2gpd
import geopandas as gpd
from . import EPSG
from .core import Dataset, geocode, replace_missing_geometries
from .regions import *

__all__ = [
    "RealEstate", 
]

class RealEstate(Dataset):
    """
    The Department of Records (DOR) published data for all documents recorded since December 06, 1999,
    including all real estate transfers in Philadelphia. 


    12/6/99 - present, updated monthly
    
    Source
    ------
    https://www.opendataphilly.org/dataset/real-estate-transfers
    """
    
    @classmethod
    def download(cls, **kwargs):

        url = "https://phl.carto.com/api/v2/sql"
        where = "extract(year from DISPLAY_DATE) = 2017"
        gdf = carto2gpd.get(url, "RTT_SUMMARY", where =where) 
        return (
            gdf.to_crs(epsg=EPSG) 
            .pipe(geocode, ZIPCodes.get())
            .pipe(geocode, Neighborhoods.get())
            .pipe(geocode, PUMAs.get())
        )

