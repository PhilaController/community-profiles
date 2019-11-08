from .core import CENSUS_REGISTRY
from .age import *
from .ancestry import *
from .earnings import *
from .education import *
from .employment import *
from .foreignborn import *
from .gini import *
from .householdincome import *
from .housing import *
from .language import *
from .medianage import *
from .medianearnings import *
from .medianhouseholdincome import *
from .mobility import *
from .percapitaincome import *
from .population import *
from .poverty import *
from .race import *
from .rentburden import *
from .analysis import *

__all__ = sorted(CENSUS_REGISTRY)


def available_census_datasets():
    """
    Return a list of the names of the available census classes.
    """
    return [CENSUS_REGISTRY[cls] for cls in sorted(CENSUS_REGISTRY)]

