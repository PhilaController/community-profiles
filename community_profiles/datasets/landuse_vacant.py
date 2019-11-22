import carto2gpd
import pandas as pd
import geopandas as gpd
from . import EPSG
from .core import Dataset, geocode, replace_missing_geometries
from .regions import *
import community_profiles.datasets as cp_data
import esri2gpd

__all__ = ["LandUse", "DissolvedLandUse", "VacantLand", "VacantBuilding"]


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
        fields = ["c_dig1"]

        gdf = carto2gpd.get(url, "land_use", fields=fields)

        return gdf.to_crs(epsg=EPSG).rename(columns={"c_dig1": "Type"})


def create_multipolygon(puma_name):
    """ Makes subsection of data depending on puma (puma_name). 
        
        Takes the types of land use (c_dig1) and creates 1 large polygon for each.
        
        Returns dataframe with each polygon (9 types of landuse so 9 different polygon). """

    puma = join.loc[join["puma_name"] == puma_name]

    poly_group = puma.dissolve(by="Type")

    return poly_group


class DissolvedLandUse(Dataset):
    """
    Dissolve the land use polygons such that each class gets
    combined into a MultiPolygon.

    The returned data should be 
    """

    @classmethod
    def download(cls, **kwargs):
        land = cp_data.LandUse.get()
        pumas = cp_data.PUMAs.get()

        join = gpd.sjoin(land, pumas, how="inner", op="within")

        list_polys = []

        for i in pumas["puma_name"]:
            list_polys.append(create_multipolygon(i))

        return pd.concat(list_polys)
           
           
           
class VacantLand(Dataset):
    """
    The location of properties across Philadelphia that are likely to be a 
    vacant lot based on an assessment of City of Philadelphia administrative datasets.
    
    Source
    ------
    https://www.opendataphilly.org/dataset/vacant-property-indicators
    """

    @classmethod
    def download(cls, **kwargs):
        
        fields = [
            "OBJECTID", 
            "ADDRESS", 
            "LAND_RANK",
        ]

        url = "https://services.arcgis.com/fLeGjb7u4uXqeF9q/arcgis/rest/services/Vacant_Indicators_Land/FeatureServer/0"
        gdf = esri2gpd.get(url, fields=fields)
        
        return ( 
             gdf.to_crs(epsg=EPSG)
            .pipe(geocode, ZIPCodes.get())
            .pipe(geocode, Neighborhoods.get())
            .pipe(geocode, PUMAs.get())
        )
               
           
class VacantBuilding(Dataset):
    """
    The location of properties across Philadelphia that are likely to be a 
    vacant building based on an assessment of City of Philadelphia administrative datasets.
    
    Source
    ------
    https://www.opendataphilly.org/dataset/vacant-property-indicators
    """

    @classmethod
    def download(cls, **kwargs):
        
        fields = [
            "OBJECTID", 
            "ADDRESS", 
            "BUILD_RANK",
        ]

        url = "https://services.arcgis.com/fLeGjb7u4uXqeF9q/arcgis/rest/services/Vacant_Indicators_Bldg/FeatureServer/0"
        gdf = esri2gpd.get(url, fields=fields)
        
        return ( 
             gdf.to_crs(epsg=EPSG)
            .pipe(geocode, ZIPCodes.get())
            .pipe(geocode, Neighborhoods.get())
            .pipe(geocode, PUMAs.get())
        )
                          

           
           
           
           
           
           
           
           
           
           
           
           
           
           
           
           


