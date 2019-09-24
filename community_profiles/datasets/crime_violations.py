import carto2gpd
import geopandas as gpd
from . import EPSG
from .core import Dataset



__all__ = ["Crime", "Shootings", "ParkingV", "StreetCodeV", "L_IV"]


class Crime(Dataset):
    """
    Crime Incidents
    Available: 2006-Present, Updated Daily 
    Selected: 2018 
    
    Source
    ------
    https://phl.carto.com/api/v2/sql?q=SELECT+*+FROM+incidents_part1_part2&filename=incidents_part1_part2&format=shp&skipfields=cartodb_id
    """

    @classmethod
    def download(cls, **kwargs):
        url = "https://phl.carto.com/api/v2/sql"
        where = "year(dispatch_date) = 2018"  ### doesn't work. function year(text) does not exist... How to change to datetime??
        gdf = carto2gpd.get(url, "incidents_part1_part2",  where=where)

        return gdf.to_crs(epsg=EPSG) 
        
    

class Shootings(Dataset):
    """
    City-wide shooting victims, including Police Officer-involved shootings.
    Available: 2015-yesterday, Updated Daily
    Selected: 2018 

    Source
    ------
    https://phl.carto.com/api/v2/sql?q=SELECT+*+FROM+shootings&filename=shootings&format=shp&skipfields=cartodb_id
    """

    @classmethod
    def download(cls, **kwargs):
        
        url = "https://phl.carto.com/api/v2/sql"
        where = "year = 2018"
        gdf = carto2gpd.get(url, "shootings",  where=where)

        return gdf.to_crs(epsg=EPSG) 
        
    
class ParkingV(Dataset):
    """
    Parking Violations
    Available: 2012-2017
    Selected: 2017

    Source
    ------
    https://phl.carto.com/api/v2/sql?q=SELECT+*+FROM+parking_violations&filename=parking_violations&format=shp&skipfields=cartodb_id
    """

    @classmethod
    def download(cls, **kwargs):
        url = "https://phl.carto.com/api/v2/sql"
        where = "year(issue_datetime) = 2017" ### function year(timestamp without time zone) does not exist
        gdf = carto2gpd.get(url, "parking_violations",  where=where)

        return gdf.to_crs(epsg=EPSG) 
        
            
        
class StreetCodeV(Dataset):
    """
    Code Violation Notices issued from the Street's department
    Available: 07-21-2009 - 12-27-2048???
    Selected: 2017

    Source
    ------
    https://phl.carto.com/api/v2/sql?q=SELECT+*+FROM+streets_code_violation_notices&
    filename=streets_code_violation_notices&format=shp&skipfields=cartodb_id
    """

    @classmethod
    def download(cls, **kwargs):
        url = "https://phl.carto.com/api/v2/sql"
        where = "year(date_added) = 2017" ### function year(date) does not exist
        gdf = carto2gpd.get(url, "streets_code_violation_notices",  where=where)

        return gdf.to_crs(epsg=EPSG) 
        
    
    
class L_IV(Dataset):
    """
    Violations issued by the Department of Licenses and Inspections 
    in reference to the Philadelphia Building Construction and OccupancyCode
    Available: 2007-present, Updated Daily 
    Selected: 2017 
    
    Source
    ------
    https://phl.carto.com/api/v2/sql?q=SELECT+*+FROM+li_violations&filename=li_violations&format=shp&skipfields=cartodb_id
    """

    @classmethod
    def download(cls, **kwargs):
        url = "https://phl.carto.com/api/v2/sql"
        where = "year(violationdate) = 2017" ### function year(date) does not exist
        gdf = carto2gpd.get(url, "li_violations",  where=where)

        return gdf.to_crs(epsg=EPSG) 
               
            
        
    