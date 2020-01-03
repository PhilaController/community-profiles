import esri2gpd
from . import EPSG
from .core import *
from .regions import *

__all__ = ["CommercialCorridors"]


class CommercialCorridors(Dataset):
    """
    Commercial corridors, centers, districts, and projects that provide
    consumer-oriented goods and services, including retail, food and beverage,
    and personal, professional, and business services.

    Notes
    -----
    Update frequency: as needed
    Last updated: 2019

    Source
    ------
    https://www.opendataphilly.org/dataset/commercial-corridors
    """

    @classmethod
    def download(cls, **kwargs):

        url = "https://services.arcgis.com/fLeGjb7u4uXqeF9q/arcgis/rest/services/Commercial_Corridors/FeatureServer/0"
        gdf = esri2gpd.get(url)

        return (
            gdf.to_crs(epsg=EPSG)
            .pipe(geocode, ZIPCodes.get(), use_centroids=True)
            .pipe(geocode, Neighborhoods.get(), use_centroids=True)
            .pipe(geocode, PUMAs.get(), use_centroids=True)
        )

