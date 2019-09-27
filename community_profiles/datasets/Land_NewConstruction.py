import carto2gpd
import geopandas as gpd
from . import EPSG
from .core import Dataset, geocode, replace_missing_geometries
from .regions import *
import community_profiles.datasets as cp_data


__all__ = ["LandUse", "NewConstruction", "DissolvedLandUse"]


class LandUse(Dataset):
    """
    Land Use
    # 1.0 Residential 
    # 2.0 Commercial
    # 3.0 Industrial 
    # 4.0 Civic/Institution
    # 5.0 Transportation
    # 6.0 Culture/Recreation
    # 7.0 Park/Open Space
    # 8.0 Water
    # 9.0 Vacant or Other
    
    Source
    ------
    https://www.opendataphilly.org/dataset/land-use
    """

    @classmethod
    def download(cls, **kwargs):

        url = "https://phl.carto.com/api/v2/sql"
        fields = ["c_dig1"]

        gdf = carto2gpd.get(url, "land_use", fields=fields)

        return gdf.to_crs(epsg=EPSG).rename(columns={"c_dig1": "Type"})


def create_multipolygon(puma_name):
    """ Makes subsection of data depending on puma (puma_name). 
        
        Takes the types of land use (c_dig1) and creates 1 large polygon for each.
        
        Returns dataframe with each polygon (9 types of landuse so 9 different polygon). """

    puma = join.loc[join["puma_name"] == puma_name]

    poly_group = puma.dissolve(by="Type")

    return poly_group


class DissolvedLandUse(Dataset):
    """
    Dissolve the land use polygons such that each class gets
    combined into a MultiPolygon.

    The returned data should be 
    """

    @classmethod
    def download(cls, **kwargs):
        land = cp_data.LandUse.get()
        pumas = cp_data.LandUse.get()

        join = gpd.sjoin(land, pumas, how="inner", op="within")

        list_polys = []

        for i in pumas["puma_name"]:
            list_polys.append(create_multipolygon(i))

        return pd.concat(list_polys)


class NewConstruction(Dataset):
    """
    Building and Zoning Permits 
    Available: 2007 to Present, Updated Daily 
    Selected: 2018 
    
    Source
    ------
    https://www.opendataphilly.org/dataset/licenses-and-inspections-building-permits
    """

    @classmethod
    def download(cls, **kwargs):

        url = "https://phl.carto.com/api/v2/sql"
        where = "extract(year from permitissuedate) = 2018 and permitdescription = 'NEW CONSTRUCTION PERMIT'"
        gdf = carto2gpd.get(url, "li_permits", where=where)

        return (
            replace_missing_geometries(gdf)
            .to_crs(epsg=EPSG)
            .pipe(geocode, ZIPCodes.get())
            .pipe(geocode, Neighborhoods.get())
            .pipe(geocode, PUMAs.get())
            .assign(
                permitissuedate=lambda df: pd.to_datetime(df.permitissuedate),
                year=lambda df: df.permitissuedate.dt.year,
            )
            .sort_values("permitissuedate", ascending=False)
            .reset_index(drop=True)
        )

