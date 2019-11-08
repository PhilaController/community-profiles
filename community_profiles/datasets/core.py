import geopandas as gpd
import pandas as pd
from abc import ABC, abstractclassmethod
import os, json
from . import EPSG
from .. import data_dir

REGISTRY = {}


class Dataset(ABC):
    """
    Abstract base class representing a dataset.

    Subclasses should define the `download` function, which is 
    responsible for downloading and returning a pandas DataFrame.

    Parameters
    ----------
    data_columns : list of str
        string column names of any datetime fields; these are converted
        automatically to pandas Datetime objects when data is loaded
    """

    date_columns = []

    def __init_subclass__(cls, **kwargs):
        """
        Register subclasses of this class in the `REGISTRY` dict.
        """
        if cls not in REGISTRY:
            REGISTRY[cls.__name__] = cls
        super().__init_subclass__(**kwargs)

    @classmethod
    def _format_data(cls, data):
        """
        An internal method to format the input dataframe. The performs 
        the following tasks:

        1. Convert from a pandas DataFrame to a geopandas GeoDataFrame, if possible
        2. Convert date columns to pandas Datetime objects

        It returns the formatted DataFrame/GeoDataFrame.
        """
        # convert to GeoDataFrame
        if "geometry" in data.columns:
            from shapely import wkt

            data.geometry = data.geometry.apply(wkt.loads)
            data = gpd.GeoDataFrame(
                data, geometry="geometry", crs={"init": f"epsg:{EPSG}"}
            )

        # convert date columns
        for col in cls.date_columns:
            data[col] = pd.to_datetime(data[col])

        return data

    @classmethod
    def meta(cls):
        """
        Dictionary of meta-data related to the dataset.
        """
        path = data_dir / cls.__name__ / "meta.json"
        if path.exists():
            return json.load(path.open(mode="r"))
        else:
            return {}

    @classmethod
    def now(cls):
        """
        Return the current datetime as a pandas Datetime object.
        """
        return str(pd.datetime.now())

    @classmethod
    def get_path(cls, **kwargs):
        """
        Return the directory path holding the data.
        """
        return data_dir / cls.__name__

    @classmethod
    def get(cls, fresh=False, **kwargs):
        """
        Load the dataset, optionally downloading a fresh copy.

        Parameters
        ---------
        fresh : bool, optional
            a boolean keyword that specifies whether a fresh copy of the 
            dataset should be downloaded
        **kwargs : 
            Additional keywords are passed to the `get_path()` function and 
            the `download()` function

        Returns
        -------
        data : DataFrame/GeoDataFrame
            the dataset as a pandas/geopandas object
        """
        # Get the folder path
        dirname = cls.get_path(**kwargs)
        if not os.path.exists(dirname):
            os.makedirs(dirname)
            fresh = True

        # Download and save a fresh copy
        if not os.path.exists(os.path.join(dirname, "data.csv")) or fresh:

            # download and save a fresh copy
            data = cls.download(**kwargs)
            data.to_csv(os.path.join(dirname, "data.csv"), index=False)

            # save the download time
            meta = {"download_time": cls.now()}
            json.dump(meta, open(os.path.join(dirname, "meta.json"), "w"))

        # Load and return the formatted data
        return cls._format_data(
            pd.read_csv(os.path.join(dirname, "data.csv"), low_memory=False)
        )

    @abstractclassmethod
    def download(cls, **kwargs):
        """
        Download and return the dataset.

        This must be defined for subclasses of the `Dataset` class.

        Returns
        -------
        data : DataFrame/GeoDataFrame
            the dataset as a data frame object
        """
        raise NotImplementedError


def geocode(df, polygons):
    """
    Geocode the input data set of Point geometries using 
    the specified polygon boundaries.

    Parameters
    ----------
    df : geopandas.GeoDataFrame
        the point data set 
    polygons : geopandas.GeoDataFrame
        the Polygon geometries
    
    Returns
    -------
    GeoDataFrame : 
        a copy of ``df`` with the data from ``polygons`` matched 
        according to the point-in-polygon matching
    """
    # convert the CRS
    polygons = polygons.to_crs(df.crs)

    valid = df.geometry.notnull()
    geocoded = gpd.sjoin(df.loc[valid], polygons, op="within", how="left").drop(
        labels=["index_right"], axis=1
    )

    return pd.concat([geocoded, df.loc[~valid]], sort=True)


def replace_missing_geometries(df):
    """
    Utility function to replace missing geometries with empty Point() objects.
    """
    from shapely.geometry import Point

    mask = df.geometry.isnull()
    empty = pd.Series(
        [Point() for i in range(mask.sum())], index=df.loc[mask, "geometry"].index
    )
    df.loc[mask, "geometry"] = empty

    return df
