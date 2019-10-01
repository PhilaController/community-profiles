import esri2gpd
import geopandas as gpd
from . import EPSG
from .core import Dataset, geocode, replace_missing_geometries
from .regions import *
import pandas as pd

__all__ = [
    "Schools",
    "SchoolScores",
]

    
class Schools(Dataset):
    """
    Philadephia's schools (all types) 
    
    Source
    ------
    https://phl.maps.arcgis.com/home/item.html?id=d46a7e59e2c246c891fbee778759717e
    """

    @classmethod
    def download(cls, **kwargs):
        
        fields = [
            "LOCATION_ID", 
            "SCHOOL_NAME", 
            "STREET_ADDRESS",
            "GRADE_LEVEL", 
            "GRADE_ORG",
            "TYPE", 
            "TYPE_SPECIFIC",
        ]

        url = "https://services.arcgis.com/fLeGjb7u4uXqeF9q/arcgis/rest/services/Schools/FeatureServer/0"
        return (
            esri2gpd.get(url, fields = fields)
            .to_crs(epsg=EPSG)   
            .pipe(geocode, ZIPCodes.get())
            .pipe(geocode, Neighborhoods.get())
            .pipe(geocode, PUMAs.get())
        )

    
    
    
class SchoolScores(Dataset):
    """
    Developed in 2019 and include data for the 2017-2018 School Progress Reports. 
    School Ratings of all public schools (district and charter). 

    Source
    ------
    https://www.philasd.org/performance/programsservices/open-data/school-performance/#school_progress_report
    """

    @classmethod
    def download(cls, **kwargs):

        url = ("https://cdn.philasd.org/offices/performance/Open_Data/School_Performance/"
                "School_Progress_Report/SPR_SY1718_School_Metric_Scores_20190129.xlsx") 
        df = pd.read_excel(url, sheet_name='SPR SY2017-2018 ES')

        return df    
 

###
###
# class SchoolSurvey(Dataset):
#     """
#     Student, parent/guardian, and teacher response data from the District-wide survey for those schools 
#     that met the response rate thresholds for 2017-2018.

#     Source
#     ------
#     https://www.philasd.org/performance/programsservices/open-data/school-performance/#school_progress_report
#     """

#     @classmethod
#     def download(cls, **kwargs):

#         url =("https://cdn.philasd.org/offices/performance/Open_Data/School_Information/"
#               "District_Wide_Survey/2017_2018_All_Respondent_Data.zip") ### doesnt work 
#         df = gpd.read_file(url)

#         return df.to_crs(epsg=EPSG)     
    

    