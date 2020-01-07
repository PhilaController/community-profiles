import carto2gpd
import geopandas as gpd
from . import EPSG
from .core import Dataset, geocode, replace_missing_geometries
from .regions import *

__all__ = ["Demolitions"]


class Demolitions(Dataset):
    """
    Inventory of building demolitions occurring within the City of Philadelphia.


    Source
    ------
    https://www.opendataphilly.org/dataset/building-demolitions
    """

    @classmethod
    def download(cls, **kwargs):

        # Query CARTO
        gdf = carto2gpd.get("https://phl.carto.com/api/v2/sql", "li_demolitions")

        return (
            gdf.to_crs(epsg=EPSG)
            .pipe(geocode, ZIPCodes.get())
            .pipe(geocode, Neighborhoods.get())
            .pipe(geocode, PUMAs.get())
        )

