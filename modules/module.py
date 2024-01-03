import pandas as pd
import numpy as np

def is_active(df: pd.DataFrame, start_date_col: pd.Timestamp, end_date_col: pd.Timestamp, lower_bound: str):
    """ 
    Returns boolean to indicate if a member is active in a certain timeframe.
    By default, the timeframe is one month,
    starting from the lower_bound to the upper_bound
    and inclusive

    Arguments:
        df -- dataframe
        start_date -- contract start date of the member
        end_date -- contract end date of the member
        lower_bound -- lower bound of the timeframe

    Returns:
        boolean indicating if the member is active on the timeframe
    """   
    
    lower_bound= pd.to_datetime(lower_bound)
    upper_bound= (lower_bound + pd.offsets.MonthEnd(0))
    
    conditions= (
        ((df[start_date_col] <= lower_bound) & (df[end_date_col] >= upper_bound)),
        ((df[start_date_col] <= lower_bound) & (df[end_date_col] <= upper_bound) & (df[end_date_col] >= lower_bound)),
        ((df[start_date_col] >= lower_bound) & (df[start_date_col] <= upper_bound) & (df[end_date_col] >= upper_bound)),
        ((df[start_date_col] >= lower_bound) & (df[end_date_col] <= upper_bound)),
        True
    )
    choices= [
        True, True, True, True, False
    ]
    return np.select(conditions, choices, default= False)

to_rename= {
    'date_of_birth': 'dob',
    'from': 'start_date',   
    'to': 'end_date',   
    'fully_paid_date': 'fp_date',   
    'membership': 'product',
    'partner_branch': 'center', 
    'partner_date_of_birth': 'dob2',
    'partner_city': 'city',
    'partner_gender': 'gender',
    'partner_household_income': 'income',
    'partner_job': 'job1',
    'partner_occupation': 'job2',
    'display_name': 'name',
}
to_drop= [
    'external_id',
    'partner_industry',
    'partner_street',
    'partner_street2',
    'partner_age'
]
center_map= {
    'Head Office': 'HO',
    'Kota Kasablanka': 'KK',
    'Sedayu City': 'SDC',
    'Pacific Place': 'PP',
    'Indonesia': 'ID',
    'Gandaria City': 'GC',
    'Living World': 'LW',
    'Dago': 'DG',
    'Pakuwon': 'PKW',
    'Central Park': 'CP',
    'Bekasi': 'BSD',
    'National Sales Team': 'NST',
    'BSD City': 'BSD',
    'Cibubur': 'CBB',
    np.NaN: 'None',
}
income_cat= pd.CategoricalDtype([
    'Below Rp 10.000.000', 
    'Rp 10.000.000 - Rp 20.000.000',
    'Rp 20.000.000 - Rp 30.000.000', 
    'Rp 30.000.000 - Rp 40.000.000',
    'Above Rp 40.000.000'
    ], ordered= True
)