import geopandas as gpd
import pandas as pd
from . import EPSG
from .core import Dataset, geocode, replace_missing_geometries
from .regions import *
import requests, zipfile, io
import community_profiles.datasets as cp_data
import numpy as np 


pumas = cp_data.PUMAs.get()  
pumas['puma_id'] = pumas['puma_id'].astype(str).str[3:].astype(np.int64)

            
__all__ = [
    "persons",
    "houses",
]

        
class persons(Dataset):
    """
    Population Records 
    2013-2017 American Community Survey 5-year Public Use Microdata Sample files 
     
    Source
    ------
    https://www2.census.gov/programs-surveys/acs/data/pums/2017/5-Year/csv_ppa.zip
    """

    
    @classmethod
    def download(cls, **kwargs):

        url = 'https://www2.census.gov/programs-surveys/acs/data/pums/2017/5-Year/csv_ppa.zip'
        r = requests.get(url)
        z = zipfile.ZipFile(io.BytesIO(r.content))
        z.extractall()
        df = pd.read_csv(z.open('psam_p42.csv'))


        return df.loc[df['PUMA'].isin(pumas['puma_id'])]
    
class houses(Dataset):
    """
    Housing Unit Records 
    2013-2017 American Community Survey 5-year Public Use Microdata Sample files 

    Source
    ------
    https://www2.census.gov/programs-surveys/acs/data/pums/2017/5-Year/csv_hpa.zip
    """


    @classmethod
    def download(cls, **kwargs):

        url = 'https://www2.census.gov/programs-surveys/acs/data/pums/2017/5-Year/csv_hpa.zip'
        r = requests.get(url)
        z = zipfile.ZipFile(io.BytesIO(r.content))
        z.extractall()
        df = pd.read_csv(z.open('psam_h42.csv'))


        return df.loc[df['PUMA'].isin(pumas['puma_id'])]