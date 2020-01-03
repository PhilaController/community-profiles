import esri2gpd
import geopandas as gpd
from . import EPSG
from .core import Dataset, geocode, replace_missing_geometries
from .regions import *

__all__ = ["RegionalRail", "BroadStLine", "MFLine", "Bus"]


class RegionalRail(Dataset):
    """
    Spring 2018 Regional Rail Rail Stations with Ridership. 
    Station ridership data is from SEPTA's 2015 Regional Rail Census.

    Source
    ------
    https://opendata.arcgis.com/datasets/64eaa4539cf4429095c2c7bf25c629a2_0.zip
    """

    @classmethod
    def download(cls, **kwargs):

        url = "https://opendata.arcgis.com/datasets/64eaa4539cf4429095c2c7bf25c629a2_0.zip"
        df = gpd.read_file(url)

        return (
            df.to_crs(epsg=EPSG)
            .pipe(geocode, ZIPCodes.get())
            .pipe(geocode, Neighborhoods.get())
            .pipe(geocode, PUMAs.get())
        )


class BroadStLine(Dataset):
    """
    Spring 2018 Broad Street Line Stations with Ridership. 
    Station ridership data is from FY17 turn-style counts and excludes free interchange riders.

    Source
    ------
    https://opendata.arcgis.com/datasets/2e9037fd5bef406488ffe5bb67d21312_0.zip
    """

    @classmethod
    def download(cls, **kwargs):

        url = "https://opendata.arcgis.com/datasets/2e9037fd5bef406488ffe5bb67d21312_0.zip"
        df = gpd.read_file(url)

        return (
            df.to_crs(epsg=EPSG)
            .pipe(geocode, ZIPCodes.get())
            .pipe(geocode, Neighborhoods.get())
            .pipe(geocode, PUMAs.get())
        )


class MFLine(Dataset):
    """
    Spring 2018 Market-Frankford Line Stations with Ridership. 
    Station ridership data is from FY17 turn-style counts and excludes free interchange riders.

    Source
    ------
    https://opendata.arcgis.com/datasets/8c6e2575c8ad46eb887e6bb35825e1a6_0.zip
    """

    @classmethod
    def download(cls, **kwargs):

        url = "https://opendata.arcgis.com/datasets/8c6e2575c8ad46eb887e6bb35825e1a6_0.zip"
        df = gpd.read_file(url)

        return (
            df.to_crs(epsg=EPSG)
            .pipe(geocode, ZIPCodes.get())
            .pipe(geocode, Neighborhoods.get())
            .pipe(geocode, PUMAs.get())
        )


class Bus(Dataset):
    """
    SEPTA Spring 2018 bus stops with ridership. Ridership contains Spring 2018 APC data where available. 
    Ridecheck data has been used to supplement gaps in the APC data.

    Source
    ------
    https://opendata.arcgis.com/datasets/5c063cd7037547659905ab1761db469e_0.zip
    """

    @classmethod
    def download(cls, **kwargs):

        url = "https://opendata.arcgis.com/datasets/5c063cd7037547659905ab1761db469e_0.zip"
        df = gpd.read_file(url)

        return (
            df.to_crs(epsg=EPSG)
            .pipe(geocode, ZIPCodes.get())
            .pipe(geocode, Neighborhoods.get())
            .pipe(geocode, PUMAs.get())
        )

