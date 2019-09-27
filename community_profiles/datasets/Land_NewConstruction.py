import carto2gpd
import geopandas as gpd
from . import EPSG
from .core import Dataset, geocode, replace_missing_geometries
from .regions import *

__all__ = [
    "LandUse",
    "NewConstruction",
]



class LandUse(Dataset):
    """
    Land Use
    # 1.0 Residential 
    # 2.0 Commercial
    # 3.0 Industrial 
    # 4.0 Civic/Institution
    # 5.0 Transportation
    # 6.0 Culture/Recreation
    # 7.0 Park/Open Space
    # 8.0 Water
    # 9.0 Vacant or Other
    
    Source
    ------
    https://www.opendataphilly.org/dataset/land-use
    """
    
    @classmethod
    def download(cls, **kwargs):

        url = "https://phl.carto.com/api/v2/sql"
        gdf = carto2gpd.get(url, "land_use") 
        
        return gdf.to_crs(epsg=EPSG) 
    
    
    
class  NewConstruction(Dataset):
    """
    Building and Zoning Permits 
    Available: 2007 to Present, Updated Daily 
    Selected: 2018 
    
    Source
    ------
    https://www.opendataphilly.org/dataset/licenses-and-inspections-building-permits
    """
    
    @classmethod
    def download(cls, **kwargs):

        url = "https://phl.carto.com/api/v2/sql"
        where = "extract(year from permitissuedate) = 2018 and permitdescription = 'NEW CONSTRUCTION PERMIT'"
        gdf = carto2gpd.get(url, "li_permits", where = where) 
        
        return g(
            replace_missing_geometries(gdf)
            .to_crs(epsg=EPSG)
            .pipe(geocode, ZIPCodes.get())
            .pipe(geocode, Neighborhoods.get())
            .pipe(geocode, PUMAs.get())
            .assign(
                permitissuedate=lambda df: pd.to_datetime(df.permitissuedate),
                year=lambda df: df.permitissuedate.dt.year,
            )
            .sort_values("permitissuedate", ascending=False)
            .reset_index(drop=True)
        )

