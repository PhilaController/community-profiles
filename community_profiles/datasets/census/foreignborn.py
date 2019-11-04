from .core import CensusDataset

__all__ = ["ForeignBorn"]


class ForeignBorn(CensusDataset):
    """
    Place of birth by nativity and citizenship status.
    """

    UNIVERSE = "total population"
    TABLE_NAME = "B05002"
    RAW_FIELDS = {"001": "universe", "002": "native", "013": "foreign_born"}

