from .age import Age
from .pop import TotalPopulation
from .foreignborn import ForeignBorn
from .race import Race
from .education import EducationalAttainment
from .language import HouseholdLanguage
from .employment import EmploymentStatus
from .income import MedianIncome
from .housevalue import MedianHouseValue
from .tenure import Tenure
from .workerclass import WorkerClass
from .poverty import Poverty
from .rentburden import RentBurden
from .gini import GiniIncomeInequality

__all__ = [
    "Age",
    "TotalPopulation",
    "ForeignBorn",
    "Race",
    "EducationalAttainment",
    "HouseholdLanguage",
    "EmploymentStatus",
    "MedianIncome",
    "MedianHouseValue",
    "Tenure",
    "WorkerClass",
    "Poverty",
    "RentBurden",
    "GiniIncomeInequality",
]


def available_census_datasets():
    """
    Return a list of the names of the available census classes.
    """
    mod = globals()
    return [mod[cls] for cls in __all__]

