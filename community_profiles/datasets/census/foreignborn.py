from .core import CensusDataset


class ForeignBorn(CensusDataset):
    """
    Native vs foreign born population.

    Source
    ------
    American Community Survey
    """

    TABLE_NAME = "B05002"
    RAW_FIELDS = {"001": "universe", "002": "native", "013": "foreign_born"}

