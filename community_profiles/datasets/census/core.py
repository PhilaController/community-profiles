from ..regions import PUMAs, CensusTracts
from ..core import Dataset, data_dir
import cenpy as cen
import os
import pandas as pd


class CensusDataset(Dataset):
    """
    A base class to represent a dataset downloaded from the Census API.
    """

    @classmethod
    def process(cls, df):
        """
        Process the raw data files, adding custom columns if desired.
        """
        return df

    @classmethod
    def get_path(cls, level="puma", year=2017):
        return os.path.join(data_dir, cls.__name__, level, str(year))

    @classmethod
    def download(cls, level="puma", **kwargs):

        return cls._query_census_api(level=level, **kwargs)

    @classmethod
    def get(cls, fresh=False, level="puma", **kwargs):
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
        allowed_levels = ["puma", "tract"]
        level = level.lower()
        if level not in allowed_levels:
            raise ValueError(f"Allowed values for 'level' are: {allowed_levels}")

        # return
        return super().get(fresh=fresh, level=level, **kwargs)

    @classmethod
    def _query_census_api(cls, level, year=2017):
        """
        Download the requested fields from the American Community Survey
        using the Census API.

        Parameters
        ----------
        variables : list of str
            the names of the census variables to download
        year : int, optional
            the year of data to download
        """
        if level == "puma":
            boundaries = PUMAs.get(year=year)
            geo_unit = "public use microdata area"
        else:
            boundaries = CensusTracts.get(year=year)
            geo_unit = "tract"

        # initialize the API
        api = cen.remote.APIConnection(f"ACSDT5Y{year}")

        # Format the variable names properly
        variables = {
            f"{cls.TABLE_NAME}_{field}E": renamed
            for field, renamed in cls.RAW_FIELDS.items()
        }

        # Query the census API to get the raw data
        df = api.query(
            cols=list(variables), geo_unit=f"{geo_unit}:*", geo_filter={"state": "42"}
        )

        # Create the ID column and remove unnecessary columns
        if level == "puma":
            df["geo_id"] = df.apply(
                lambda row: row["state"] + row["public use microdata area"], axis=1
            )
            df = df.drop(labels=["state", "public use microdata area"], axis=1)
        else:
            df["geo_id"] = df.apply(
                lambda row: row["state"] + row["county"] + row["tract"], axis=1
            )
            df = df.drop(labels=["state", "county", "tract"], axis=1)

        # set the boundary ID as a string
        boundaries["geo_id"] = boundaries["geo_id"].astype(str)

        # Merge the data with the boundaries
        df = boundaries.merge(df, on="geo_id")

        # Convert columns from strings to numbers
        for col in variables:
            df[col] = pd.to_numeric(df[col])

        # Return the processed data
        return cls.process(df.rename(columns=variables))
