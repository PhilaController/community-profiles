import esri2gpd
import geopandas as gpd
from . import EPSG
from .core import Dataset, geocode
from .regions import *


__all__ = ["StreetDefectRepairRating", "LitterIndex"]


class StreetDefectRepairRating(Dataset):
    """
    Street Defect Repair Rating

    Notes
    -----
    Rates streets from 0 to 100 based on the number of street defect repairs
    since 2013, accounting for the different lengths of streets across the city.
    Streets with a high rating have had more defect repairs than average since
    2013, while streets with a lower rating have had fewer repairs than the
    citywide average over that time period.

    Source
    ------
    http://phl.maps.arcgis.com/home/item.html?id=288d67ea531c4e1a96ebe43a78b97ca8
    """

    @classmethod
    def download(cls, **kwargs):

        url = "https://services.arcgis.com/fLeGjb7u4uXqeF9q/arcgis/rest/services/Street_Defect_Rating/FeatureServer/0"
        gdf = esri2gpd.get(url)

        return (
            gdf.to_crs(epsg=EPSG)
            .pipe(geocode, ZIPCodes.get())
            .pipe(geocode, Neighborhoods.get())
            .pipe(geocode, PUMAs.get())
        )


class LitterIndex(Dataset):
    """
    Litter Index scores calculated for each street hundred-block.
    
    Notes
    -----
    Time period: 2017-2018

    Source
    ------
    https://www.opendataphilly.org/dataset/litter-index
    """

    @classmethod
    def download(cls, **kwargs):

        url = "https://services.arcgis.com/fLeGjb7u4uXqeF9q/arcgis/rest/services/Litter_Index_Blocks/FeatureServer/0"
        return (
            esri2gpd.get(url)
            .to_crs(epsg=EPSG)
            .pipe(geocode, ZIPCodes.get())
            .pipe(geocode, Neighborhoods.get())
            .pipe(geocode, PUMAs.get())
        )

