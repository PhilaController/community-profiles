from . import EPSG
from .. import data_dir
from .core import Dataset, geocode, replace_missing_geometries
from .regions import *
import pandas as pd
import geopandas as gpd
import numpy as np
from shapely.geometry import Point
import tempfile
import requests, zipfile, io


__all__ = ["Schools", "SchoolScores", "SchoolSurvey", "GraduationRates"]


class Schools(Dataset):
    """
    Philadephia's schools (all types) 
    
    SY 2019-2020

    Source
    ------
    https://phl.maps.arcgis.com/home/item.html?id=d46a7e59e2c246c891fbee778759717e
    """

    @classmethod
    def download(cls, **kwargs):

        # Load the raw data
        url = "https://cdn.philasd.org/offices/performance/Open_Data/School_Information/School_List/2019-2020%20Master%20School%20List%20(20191218).csv"
        df = pd.read_csv(url)

        # Convert GPS column to geometry
        df["geometry"] = df["GPS Location"].apply(
            lambda x: Point(*tuple(map(float, x.split(",")[::-1])))
        )

        # Return a GeoDataFrame
        return gpd.GeoDataFrame(
            df, geometry="geometry", crs={"init": "epsg:4326"}
        ).to_crs(epsg=EPSG)


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

        # Load the raw data
        url = (
            "https://cdn.philasd.org/offices/performance/Open_Data/School_Performance/"
            "School_Progress_Report/SPR_SY1718_School_Metric_Scores_20190129.xlsx"
        )
        df = pd.read_excel(url, sheet_name="SPR SY2017-2018")

        # Load geometries for schools and merge them in
        schools = Schools.get(fresh=True)[
            ["ULCS Code", "Governance", "School Level", "geometry"]
        ]

        for a in [schools, df]:
            a["ULCS Code"] = a["ULCS Code"].astype(str)
        df = schools.merge(df, on="ULCS Code")

        # Make overall score a float (non-numbers are set to NaN)
        df["Overall Score"] = pd.to_numeric(df["Overall Score"], errors="coerce")

        return df


def _extract_question_data(df, text):
    """
    Internal function to extract question responses from a school survey.

    Parameters
    ----------
    df : DataFrame
        the raw survey data
    text : str
        the question snippet we are using to identify the responses to return.
    """

    # Trim to only columns that start with Q
    cols = df.filter(regex="^Q.*", axis=1)

    # # Combine the first two rows into a single string
    questions = (
        cols.iloc[[0, 1]]
        .fillna("")
        .astype(str)
        .apply(lambda col: " ".join(col), axis=0)
    )

    # # Find the exact question that contains the input text string
    matches = questions.str.lower().str.contains(text.lower())

    # Zero matches is bad
    if matches.sum() == 0:
        matches = questions == text
        if matches.sum() == 0:
            raise ValueError(f"No matching question for question '{text}'")

    # More than one match is also bad
    if matches.sum() > 1:
        raise ValueError(
            f"Input text '{text}' matched multiple questions, please be more specific."
        )

    # Figure out the question number from the index
    # This is how we will know which columns to extract from the raw data
    question_num = questions.loc[matches].index[0]
    question_text = questions.loc[matches].squeeze()

    # Extract the column we want + the next 8 columns
    i = list(df.columns).index(question_num)
    valid_cols = list(df.columns[:2]) + list(df.columns[i : i + 8])
    subset = df[valid_cols]

    # Start
    start = subset.index[subset[subset.columns[0]].str.contains("ULCS Code", na=False)][
        0
    ]
    categories = subset.iloc[start - 1].dropna().tolist()

    # Re-format into tidy format
    # We need to handle the "Count" and "Row N %" columns separately
    combined = []
    for label in ["Count", "Row N %"]:

        # Get the cols containing the "Count" or "Row N %" data
        cols = (
            subset.columns[[0, 1]].tolist()  # ULCS Code and School Name
            + subset.columns[subset.iloc[start].str.contains(label, na=False)].tolist()
        )
        subset2 = subset.iloc[start + 1 :][cols]

        # Set the columns to the categories
        subset2.columns = ["ULCS Code", "School Name"] + categories

        # Convert from a wide to tidy format
        melted = subset2.melt(
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
    Student, parent/guardian, and teacher response data from the District-wide
    survey for those schools that met the response rate thresholds

    Source
    ------
    https://www.philasd.org/performance/programsservices/open-data/school-performance/#school_progress_report
    """

    SCHOOL_YEAR = [2018, 2019]

    @classmethod
    def get_path(cls, kind="student"):
        return data_dir / cls.__name__ / kind

    @classmethod
    def get(cls, fresh=False, kind="student"):
        """
        Load the dataset, optionally downloading a fresh copy.
        
        Parameters
        ---------
        fresh : bool, optional
            a boolean keyword that specifies whether a fresh copy of the 
            dataset should be downloaded
        kind : str, optional
            kind of responses: 'student', 'parent', or 'teacher'
        """
        # Verify input level
        allowed = ["student", "parent", "teacher"]
        if kind not in allowed:
            raise ValueError(f"Allowed values for 'lind' are: {allowed}")

        # return
        return cls.process(super().get(fresh=fresh, kind=kind), kind=kind)

    @classmethod
    def download(cls, **kwargs):

        # what kind of response to return?
        kind = kwargs.get("kind", "student")

        # download to a temporary directory first
        with tempfile.TemporaryDirectory() as tmpdirname:

            # Download the ZIP file
            url = (
                "https://cdn.philasd.org/offices/performance/Open_Data/School_Information/"
                f"District_Wide_Survey/{cls.SCHOOL_YEAR[0]}_{cls.SCHOOL_YEAR[1]}_All_Respondent_Data.zip"
            )
            r = requests.get(url)
            z = zipfile.ZipFile(io.BytesIO(r.content))
            z.extractall(path=tmpdirname)

            # tags
            tag = "-".join(map(str, cls.SCHOOL_YEAR))  # this is 2018-2019
            sheet_tag = "".join(map(lambda x: str(x)[-2:], cls.SCHOOL_YEAR))  # 1819
            kind = kind.capitalize()

            return pd.read_excel(
                z.open(f"{tag} {kind} School Level.xlsx"),
                sheet_name=f"{sheet_tag} {kind}",
            )

    @classmethod
    def process(cls, df, kind="student"):

        if kind == "parent":
            questions = ["quality of education", "unsafe walking route to school"]
        elif kind == "student":
            questions = [
                "The school building is in good condition",
                "My school is clean",
                "I feel safe in the neighborhood surrounding my school",
                "I feel safe going to and from school",
            ]
        elif kind == "teacher":
            questions = [
                "School crime/safety",
                "Students have inadequate basic skills or prior preparation",
                "Neighborhood crime/safety",
            ]

        # Combine all of the questions
        out = []
        for q in questions:
            extract = _extract_question_data(df, q)
            extract["question_tag"] = q
            out.append(extract)
        out = pd.concat(out)

        # Load geometries for schools and merge them in
        schools = Schools.get(fresh=True)[
            ["ULCS Code", "Governance", "School Level", "geometry"]
        ]
        for a in [schools, out]:
            a["ULCS Code"] = a["ULCS Code"].astype(str)
        return schools.merge(out, on="ULCS Code")


class GraduationRates(Dataset):
    """
    Developed in 2019 for the 2017-2018 counts and percentages of students who have graduated in four years 
    and in six years by school. 
    
    Divided into ELL status, IEP status, Economically Disadvantaged Status, Grade and Ethnicity. 
    
    Students are attributed to the last school they attend in the four- or six-year window, which ends on September 30 of 
    their expected graduation year. 
    
    Note: Does not include Charter Schools.

    Source
    ------
    https://www.philasd.org/performance/programsservices/open-data/school-performance/#school_graduation_rates
   
    """

    @classmethod
    def download(cls, **kwargs):

        # Load the raw data
        url = (
            "https://cdn.philasd.org/offices/performance/Open_Data/School_Performance/Graduation_Rates/"
            "FT9%20SY2014-15%20Grad%20Rates%20Suppressed.csv"
        )

        df = pd.read_csv(url).rename(columns={"srcschoolid": "SRC School ID"})
        df["SRC School ID"] = df["SRC School ID"].astype(str)

        # Load geometries for schools and merge them in
        schools = Schools.get(fresh=True)[
            ["ULCS Code", "SRC School ID", "Governance", "School Level", "geometry"]
        ]
        schools["SRC School ID"] = schools["SRC School ID"].astype(str)
        return schools.merge(df, on="SRC School ID")

