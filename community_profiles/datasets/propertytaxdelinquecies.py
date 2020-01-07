import carto2gpd
import geopandas as gpd
from . import EPSG
from .core import Dataset, geocode, replace_missing_geometries
from .regions import *

__all__ = ["TaxDelinquencies"]


class TaxDelinquencies(Dataset):
    """
    Properties with tax delinquencies, including those that are in payment
    agreements.

    Source
    ------
    https://www.opendataphilly.org/dataset/property-tax-delinquencies
    """

    @classmethod
    def download(cls, **kwargs):

        url = "https://phl.carto.com/api/v2/sql"
        gdf = carto2gpd.get(url, "real_estate_tax_delinquencies")

        return (
            gdf.to_crs(epsg=EPSG)
            .pipe(geocode, ZIPCodes.get())
            .pipe(geocode, Neighborhoods.get())
            .pipe(geocode, PUMAs.get())
        )

