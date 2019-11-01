from .core import CensusDataset
import collections


class Tenure(CensusDataset):
    """
    Occupied housing units. Owner or renter.
    """

    UNIVERSE = "Occupied Housing Units"
    TABLE_NAME = "B25003"
    RAW_FIELDS = collections.OrderedDict(
        {"001": "universe", "002": "owner_occupied", "003": "renter_occupied"}
    )

