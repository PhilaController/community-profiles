import esri2gpd
import geopandas as gpd
from . import EPSG
from .core import Dataset, geocode
from .regions import *

__all__ = ["RegionalRail", "SubwayBroadSt", "SubwayMFL", "Bus"]


class RegionalRail(Dataset):
    """
    Spring 2018 Regional Rail Rail Lines with Ridership. Route ridership and
    revenue information is from FY2017. Data is from SEPTA's Revenue & Ridership
    Department.

    Source
    ------
    http://septaopendata-septa.opendata.arcgis.com/datasets/septa-regional-rail-lines
    """

    @classmethod
    def download(cls, **kwargs):

        url = "https://opendata.arcgis.com/datasets/48b0b600abaa4ca1a1bacf917a31c29a_0.zip"
        df = gpd.read_file(url)

        return (
            df.to_crs(epsg=EPSG)
            .pipe(geocode, ZIPCodes.get())
            .pipe(geocode, Neighborhoods.get())
            .pipe(geocode, PUMAs.get())
        )


class SubwayBroadSt(Dataset):
    """
    Spring 2018 Broad Street Line with Ridership. Route ridership and revenue
    information is from FY2017. Data is from SEPTA's Revenue & Ridership
    Department.

    Source
    ------
    http://septaopendata-septa.opendata.arcgis.com/datasets/septa-broad-street-line
    """

    @classmethod
    def download(cls, **kwargs):

        url = "https://opendata.arcgis.com/datasets/c051c18bb15444b6861a93fd247dde3d_0.zip"
        df = gpd.read_file(url)

        return (
            df.to_crs(epsg=EPSG)
            .pipe(geocode, ZIPCodes.get())
            .pipe(geocode, Neighborhoods.get())
            .pipe(geocode, PUMAs.get())
        )


class SubwayMFL(Dataset):
    """
    Spring 2018 Market Frankford Line with Ridership. Route ridership and
    revenue information is from FY2017. Data is from SEPTA's Revenue & Ridership
    Department.

    Source
    ------
    http://septaopendata-septa.opendata.arcgis.com/datasets/septa-market-franford-line
    """

    @classmethod
    def download(cls, **kwargs):

        url = "https://opendata.arcgis.com/datasets/6f4ae63a492c407eb95a9e56a6750e7f_0.zip"
        df = gpd.read_file(url)

        return (
            df.to_crs(epsg=EPSG)
            .pipe(geocode, ZIPCodes.get())
            .pipe(geocode, Neighborhoods.get())
            .pipe(geocode, PUMAs.get())
        )


class Bus(Dataset):
    """
    SEPTA Spring 2018 bus stops with ridership. Ridership contains Spring 2018
    APC data where available. Ridecheck data has been used to supplement gaps in
    the APC data.

    Source
    ------
    http://septaopendata-septa.opendata.arcgis.com/datasets/septa-bus-stops
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

