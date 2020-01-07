import esri2gpd
import geopandas as gpd
from . import EPSG
from .core import *
from .regions import *


__all__ = ["StreetDefectRepairRating", "LitterIndex", "PavedMiles"]


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


class PavedMiles(Dataset):
    """
    The number of miles paved from 2013 to 2018 in the
    City of Philadelphia.

    Notes
    -----
    Excludes PennDOT managed roads, so only includes
    the "local" and "FAM" networks.
    """

    @classmethod
    def get_path(cls, level="tract"):
        return data_dir / cls.__name__ / str(level)

    @classmethod
    def download(cls, level="tract"):

        path = cls.get_path(level=level)
        return pd.read_csv(path / "data.csv")

    @classmethod
    def get(cls, fresh=False, level="tract"):
        """
        Load the dataset, optionally downloading a fresh copy.

        Parameters
        ---------
        fresh : bool, optional
            a boolean keyword that specifies whether a fresh copy of the 
            dataset should be downloaded
        leve : str, optional
            the aggregation level, one of 'tract', 'nta', 'puma', or 'city'
        """
        allowed = ["tract", "nta", "puma", "city"]
        if level not in allowed:
            raise ValueError(f"allowed values for 'level' are: {allowed}")

        return super().get(fresh=fresh, level=level)
