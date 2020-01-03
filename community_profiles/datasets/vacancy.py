import esri2gpd
from . import EPSG
from .core import *
from .regions import *

__all__ = ["VacantLand", "VacantBuildings"]


class VacantLand(Dataset):
    """
    The location of properties across Philadelphia that are likely to be a
    vacant lot based on an assessment of City of Philadelphia administrative
    datasets.

    Notes
    -----
    Update frequency: monthly

    Source
    ------
    https://www.opendataphilly.org/dataset/vacant-property-indicators
    """

    @classmethod
    def download(cls, **kwargs):

        url = "https://services.arcgis.com/fLeGjb7u4uXqeF9q/arcgis/rest/services/Vacant_Indicators_Land/FeatureServer/0"

        return (
            esri2gpd.get(url)
            .to_crs(epsg=EPSG)
            .pipe(geocode, ZIPCodes.get())
            .pipe(geocode, Neighborhoods.get())
            .pipe(geocode, PUMAs.get())
        )


class VacantBuildings(Dataset):
    """
    The location of properties across Philadelphia that are likely to be a
    vacant building based on an assessment of City of Philadelphia
    administrative datasets.

    Notes
    -----
    Update frequency: monthly

    Source
    ------
    https://www.opendataphilly.org/dataset/vacant-property-indicators
    """

    @classmethod
    def download(cls, **kwargs):

        url = "https://services.arcgis.com/fLeGjb7u4uXqeF9q/arcgis/rest/services/Vacant_Indicators_Bldg/FeatureServer/0"
        gdf = esri2gpd.get(url)

        return (
            gdf.to_crs(epsg=EPSG)
            .pipe(geocode, ZIPCodes.get())
            .pipe(geocode, Neighborhoods.get())
            .pipe(geocode, PUMAs.get())
        )

