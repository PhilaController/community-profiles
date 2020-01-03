import esri2gpd
from . import EPSG
from .core import *
from .regions import *


__all__ = ["CityOwnedFacilities", "Parks", "Hospitals", "HealthCenters"]


class CityOwnedFacilities(Dataset):
    """
    An inventory of buildings and other fixed assets owned, leased, or operated
    by the City of Philadelphia including buildings, structures, and properties.

    Notes
    -----
    Date range: 2000 to 2016
    Last updated: 2016

    Source
    ------
    https://www.opendataphilly.org/dataset/city-facilities-master-facilities-database
    """

    @classmethod
    def download(cls, **kwargs):

        url = "https://services.arcgis.com/fLeGjb7u4uXqeF9q/arcgis/rest/services/City_Facilities_pub/FeatureServer/0"

        return (
            esri2gpd.get(url)
            .to_crs(epsg=EPSG)
            .pipe(geocode, ZIPCodes.get())
            .pipe(geocode, Neighborhoods.get())
            .pipe(geocode, PUMAs.get())
        )


class Parks(Dataset):
    """
    Philadelphia Parks and Recreation owned/maintained buildings and facilities
    that can be used for programming and inventory purposes.

    Notes
    -----
    Update frequency: monthly

    Source
    ------
    https://www.opendataphilly.org/dataset/parks-and-recreation-assets
    """

    @classmethod
    def download(cls, **kwargs):

        url = "https://services.arcgis.com/fLeGjb7u4uXqeF9q/arcgis/rest/services/PPR_Assets/FeatureServer/0"
        return (
            esri2gpd.get(url, fields=["OBJECTID", "ASSET_NAME", "SITE_NAME", "ADDRESS"])
            .to_crs(epsg=EPSG)
            .pipe(geocode, ZIPCodes.get())
            .pipe(geocode, Neighborhoods.get())
            .pipe(geocode, PUMAs.get())
        )


class Hospitals(Dataset):
    """
    Philadephia's hospitals 
    
    Source
    ------
    https://phl.maps.arcgis.com/home/item.html?id=df8dc18412494e5abbb021e2f33057b2
    """

    @classmethod
    def download(cls, **kwargs):

        url = "https://services.arcgis.com/fLeGjb7u4uXqeF9q/arcgis/rest/services/Hospitals/FeatureServer/0"

        return (
            esri2gpd.get(url)
            .to_crs(epsg=EPSG)
            .pipe(geocode, ZIPCodes.get())
            .pipe(geocode, Neighborhoods.get())
            .pipe(geocode, PUMAs.get())
        )


class HealthCenters(Dataset):
    """
    Federally qualified health centers.

    Notes
    -----
    Update frequency: yearly

    Source
    ------
    https://www.opendataphilly.org/dataset/health-centers
    """

    @classmethod
    def download(cls, **kwargs):

        url = "https://services.arcgis.com/fLeGjb7u4uXqeF9q/arcgis/rest/services/Health_Centers/FeatureServer/0"
        return (
            esri2gpd.get(url)
            .to_crs(epsg=EPSG)
            .pipe(geocode, ZIPCodes.get())
            .pipe(geocode, Neighborhoods.get())
            .pipe(geocode, PUMAs.get())
        )

