from phlcensus.acs import *
from phlcensus.economic import DetailedLODES, SummaryLODES


def available_census_datasets():
    """
    Return a list of the names of the available census classes.
    """
    from phlcensus import DATASETS

    keys = list(globals().keys())
    return [DATASETS[cls] for cls in sorted(DATASETS) if cls in keys]
