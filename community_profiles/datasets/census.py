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
        df = (df.loc[df['PUMA']
                    .isin(pumas['puma_id'])])
        df = df.loc[:, ['PUMA',
                        'PWGTP',
                        'AGEP', 
                        'SEX', 
                        'NATIVITY',
                        'RAC1P',
                        'HISP' ,
                        'SCHL',
                        'ENG',
                        'ESR',
                        'JWMNP',
                        'JWTR']
                   ]        
        df['SEX'] = df['SEX'].map({1 : 'male',  
                                   2 : 'female'}) 
        df['NATIVITY'] = df['NATIVITY'].map({1 : 'non-foreign', 
                                             2 : 'foreign'}) 
        df['RAC1P'] = df['RAC1P'].map({1 : 'white alone',
                                       2 : 'black alone',
                                       3 : 'american indian alone',
                                       4 : 'alaska native alone',
                                       5 : 'american indian and alaska native tribes specified',
                                       6 : 'asian alone',
                                       7 : 'native hawaiian/other pacific alone',
                                       8 : 'some other race alone',
                                       9 : 'two or more races'})
        df['JWTR'] = df['JWTR'].map({1 : 'car,truck,van',
                                        2 : 'bus or trolley',
                                        3 : 'streetcar',
                                        4 : 'subway or elevated', 
                                        5 : 'railroad',
                                        6 : 'ferryboat',
                                        7 : 'taxicab',
                                        8 : 'motorcycle',
                                        9 : 'bicycle', 
                                        10 : 'walk',
                                        11 : 'work at home',
                                        12 : 'other'})               
        return df.rename(columns={'PWGTP': 'person_weight', 'RAC1P': 'RACE', 'JWTR' : 'COM_TYP', 'JWMNP' : 'COM_TIME', 'ESR': 'EMPLOY'}) 
    
    
    
    
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
        df =  (df.loc[df['PUMA']
                     .isin(pumas['puma_id'])])
        df = df.loc[:, ['PUMA', 
                        'WGTP', 
                        'HINCP',
                        'GRNTP' ]
                   ]
        return df.rename(columns={'WGTP': 'house_weight', 'HINCP' : 'house_income', 'GRNTP' : 'month_rent'}) 
        
        