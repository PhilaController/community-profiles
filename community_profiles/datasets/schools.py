import esri2gpd
import geopandas as gpd
from . import EPSG
from .core import Dataset, geocode, replace_missing_geometries
from .regions import *
import pandas as pd
import numpy as np 
import tempfile
import requests, zipfile, io




__all__ = [
    "Schools",
    "SchoolScores",
    "SchoolSurvey",
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

    
    
def extract_question_data(df, text):
    
    # Trim to only columns that start with Q
    cols = df.filter(regex="^Q.*", axis=1)

    # Combine the first two rows into a single string
    questions = cols.iloc[[0, 1]].apply(lambda col: " ".join(col), axis=0)

    # Find the exact question that contains the input text string
    matches = questions.str.contains(text)

    # Zero matches is bad
    if matches.sum() == 0:
            matches = questions == text
            if matches.sum() == 0:
                raise ValueError("No matching question")

    # More than one match is also bad
    if matches.sum() > 1:
        raise ValueError(
            "Input text matched multiple questions, please be more specific."
        )

    # Figure out the question number from the index
    # This is how we will know which columns to extract from the raw data
    question_num = questions.loc[matches].index[0]
    question_text = questions.loc[matches].squeeze()

    # Extract the column we want + the next 8 columns
    i = list(df.columns).index(question_num)
    valid_cols = list(df.columns[:2]) + list(df.columns[i : i + 8])
    subset = df[valid_cols]

    # Extract out the categories (Rarely, Sometimes, etc)
    categories = list(subset.iloc[2].dropna())  # remove first entry "School Name"
    categories = categories[-4:]
    
    # Re-format into tidy format
    # We need to handle the "Count" and "Row N %" columns separately
    combined = []
    for label in ["Count", "Row N %"]:

        # Get the cols containing the "Count" or "Row N %" data
        cols = subset.columns[subset.iloc[3].str.contains(label, na=False)]
        cols = list(subset.columns[:2]) + list(cols)  # Add in School Name and ULCS Code
        subset2 = subset[cols]

        # Set the columns to the categories
        subset2.columns = ["ULCS Code", "School Name"] + categories

        # Convert from a wide to tidy format
        melted = subset2.iloc[4:].melt(
            id_vars=["School Name", "ULCS Code"],
            var_name="category",
            value_name="value",
        )

        # All of the rows are this type of data (Count or Row N %)
        melted["kind"] = label

        # Save so we can concat later
        combined.append(melted)

    # Combine the Count and Row N % data into one DataFrame
    out = pd.concat(combined, axis=0)

    # Each row will get the same question text too
    out["question"] = question_text

    return out
    
    
    
    
    
class SchoolSurvey(Dataset):
    """
    Student, parent/guardian, and teacher response data from the District-wide survey for those schools 
    that met the response rate thresholds for 2017-2018.

    Source
    ------
    https://www.philasd.org/performance/programsservices/open-data/school-performance/#school_progress_report
    """

    @classmethod
    def download(cls, **kwargs):


        with tempfile.TemporaryDirectory() as tmpdirname:
            url = ('https://cdn.philasd.org/offices/performance/Open_Data/School_Information/'
                   'District_Wide_Survey/2017_2018_All_Respondent_Data.zip')
            r = requests.get(url)
            z = zipfile.ZipFile(io.BytesIO(r.content))
            z.extractall(path = tmpdirname)
            
            df_p = pd.read_excel(z.open('2017-2018 Parent School Level.xlsx'), sheet_name='1718 Parent')
            df_s = pd.read_excel(z.open('2017-2018 Student School Level.xlsx'), sheet_name='1718 Student')
            df_t = pd.read_excel(z.open('2017-2018 Teacher School Level.xlsx'), sheet_name='1718 Teacher')
            
            
            parent_q = [
                    "I am pleased with the quality of education my child's school is providing for my child.", 
                    "Unsafe walking route to school",
                   ]

            student_q = [
                    "The school building is in good condition.", 
                    "My school is clean.", 
                    "I feel safe in the neighborhood surrounding my school.",
                    "I feel safe going to and from school.",
                    ] 

            teacher_q = [
                    ("To what extent do you consider each of the following factors\xa0a challenge"
                    " to student learning in your school? School crime/safety"),
                    ("To what extent do you consider each of the following factors\xa0a "
                     "challenge to student learning in your school? Lack of computers or other technological resources"),
                    ("To what extent do you consider each of the following factors a challenge to student learning in your school?"
                      " Neighborhood crime/safety"),
                    ]
            
            parent_df = []
            for q in parent_q:
                    parent_df.append(extract_question_data(df_p, q))
            df1 = pd.concat(parent_df)
                    
            student_df = []
            for q in student_q:
                    student_df.append(extract_question_data(df_s, q))
            df2 = pd.concat(student_df)

            teacher_df = []
            for q in teacher_q:
                    teacher_df.append(extract_question_data(df_t, q))                    
            df3 = pd.concat(teacher_df)       
                    

        return pd.concat([df1,df2, df3]) 
    

    