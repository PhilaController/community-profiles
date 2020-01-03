import carto2gpd
from . import EPSG
from .core import *
from .regions import *

__all__ = ["RealEstateTransfers"]


class RealEstateTransfers(DatasetWithYear):
    """
    The Department of Records (DOR) published data for all documents recorded
    since December 06, 1999, including all real estate transfers in
    Philadelphia. 

    Notes
    ------
    Available: 2000 to present
    Update frequency: monthly

    Source
    ------
    https://www.opendataphilly.org/dataset/real-estate-transfers
    """

    date_columns = ["receipt_date", "recording_date", "document_date", "display_date"]

    @classmethod
    def download(cls, year=2018):

        gdf = carto2gpd.get(
            "https://phl.carto.com/api/v2/sql",
            "RTT_SUMMARY",
            where=f"extract(year from DISPLAY_DATE) = {year}",
        )
        return (
            gdf.to_crs(epsg=EPSG)
            .drop(labels=["zip_code"], axis=1)
            .pipe(geocode, ZIPCodes.get())
            .pipe(geocode, Neighborhoods.get())
            .pipe(geocode, PUMAs.get())
        )

