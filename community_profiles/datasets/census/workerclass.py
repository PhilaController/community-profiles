from .core import CensusDataset
import collections



class WorkerClass(CensusDataset):
    """
    Sex by Class of Worker for the Civilian Employed Population 16 Years and Over.
    """
    TABLE_NAME = 'B24080'
    RAW_FIELDS = collections.OrderedDict({
        '001': "universe",
        '002': "male_total",
        '003': "male_private_for_profit_wage_and_salary",
        '004': "male_employee_of_private_company",
        '005': "male_selfemployed_in_own_incorporated_business",
        '006': "male_private_not_for_profit_wage_and_salary",
        '007': "male_local_government",
        '008': "male_state_government",
        '009': "male_federal_government",
        '010': "male_selfemployed_in_own_not_incorporated_business",
        '011': "male_unpaid_family_workers",
        '012': "female_total",
        '013': "female_private_for_profit_wage_and_salary",
        '014': "female_employee_of_private_company",
        '015': "female_selfemployed_in_own_incorporated_business",
        '016': "female_private_not_for_profit_wage_and_salary",
        '017': "female_local_government",
        '018': "female_state_government",
        '019': "female_federal_government",
        '020': "female_selfemployed_in_own_not_incorporated_business",
        '021': "female_unpaid_family_workers"
        }
    )
    
    @classmethod
    def process(cls, df):
    
        return df
    