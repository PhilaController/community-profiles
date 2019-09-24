import esri2gpd
import geopandas as gpd
from . import EPSG
from .core import Dataset

__all__ = ["Neighborhoods", "ZIPCodes", "CityLimits", "PUMAs"]


class PUMAs(Dataset):
    """
    The boundary regions for the Public Use Microdata Areas (PUMAs) 
    in Philadelphia from the 2010 Census.

    Source
    ------
    https://usa.ipums.org/usa/resources/volii/shapefiles/ipums_puma_2010.zip
    """

    @classmethod
    def download(cls, **kwargs):
        """
        Download the PUMA boundaries
        """
        # Download the raw data (all regions)
        url = "https://usa.ipums.org/usa/resources/volii/shapefiles/ipums_puma_2010.zip"
        df = gpd.read_file(url)

        # Trim
        in_philly = df.Name.str.contains("Philadelphia")
        df = df.loc[in_philly]

        # Return
        return df.loc[:, ["GEOID", "Name", "geometry"]].rename(
            columns={"GEOID": "puma_id", "Name": "puma_name"}
        )


class CityLimits(Dataset):
    """
    Philadelphia's city limits.

    Source
    ------
    http://phl.maps.arcgis.com/home/item.html?id=405ec3da942d4e20869d4e1449a2be48
    """

    @classmethod
    def download(cls, **kwargs):

        url = "https://services.arcgis.com/fLeGjb7u4uXqeF9q/arcgis/rest/services/City_Limits/FeatureServer/0"
        return esri2gpd.get(url).to_crs(epsg=EPSG)


class Neighborhoods(Dataset):
    """
    Polygons representing Philadelphia's neighborhoods.

    Notes
    -----
    These are Zillow-based neighborhoods.

    Source
    ------
    https://phl.maps.arcgis.com/home/item.html?id=ab9d26be1df8486c8d5d706fb32b33d5
    """

    @classmethod
    def download(cls, **kwargs):

        url = "https://services.arcgis.com/fLeGjb7u4uXqeF9q/ArcGIS/rest/services/Philly_Neighborhoods/FeatureServer/0"
        return (
            esri2gpd.get(url, fields=["MAPNAME"])
            .to_crs(epsg=EPSG)
            .rename(columns={"MAPNAME": "neighborhood"})
        )


class ZIPCodes(Dataset):
    """
    Polygons representing Philadelphia's ZIP codes.

    Notes
    -----
    These are from the 2018 Census ZIP Code Tabulation Areas (ZCTAs).

    Source
    ------
    https://phl.maps.arcgis.com/home/item.html?id=ab9d26be1df8486c8d5d706fb32b33d5
    """

    @classmethod
    def download(cls, **kwargs):

        url = "https://services.arcgis.com/fLeGjb7u4uXqeF9q/arcgis/rest/services/Philadelphia_ZCTA_2018/FeatureServer/0"
        return esri2gpd.get(url, fields=["zip_code"]).to_crs(epsg=EPSG)
    
    

