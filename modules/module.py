import pandas as pd
import numpy as np


to_rename = {
    "date_of_birth": "dob",
    "from": "start_date",
    "to": "end_date",
    "fully_paid_date": "fp_date",
    "membership": "product",
    "partner_branch": "center",
    "partner_date_of_birth": "dob2",
    "partner_city": "city",
    "partner_gender": "gender",
    "partner_household_income": "income",
    "partner_job": "job1",
    "partner_occupation": "job2",
    "display_name": "name",
}
to_drop = [
    "external_id",
    "partner_industry",
    "partner_street",
    "partner_street2",
    "partner_age",
]
center_map = {
    "HEAD OFFICE": "HO",
    "KOTA KASABLANKA": "KK",
    "SEDAYU CITY": "SDC",
    "PACIFIC PLACE": "PP",
    "INDONESIA": "ID",
    "GANDARIA CITY": "GC",
    "LIVING WORLD": "LW",
    "DAGO": "DG",
    "PAKUWON": "PKW",
    "CENTRAL PARK": "CP",
    "BEKASI": "SMB",
    "NATIONAL SALES TEAM": "NST",
    "BSD CITY": "BSD",
    "CIBUBUR": "CBB",
    "SIMATUPANG": "TBS",
    "INDIES": "INDIES",
    np.nan: "NONE",
}
jkt_1 = ["PP", "SDC", "KG"]
jkt_2 = ["GC", "LW", "BSD", "TBS", "CP"]
jkt_3 = ["KK", "CBB", "SMB"]
bdg = ["DG"]
sby = ["PKW"]
centers = jkt_1 + jkt_2 + jkt_3 + bdg + sby

income_cat = pd.CategoricalDtype(
    [
        "Below Rp 10.000.000",
        "Rp 10.000.000 - Rp 20.000.000",
        "Rp 20.000.000 - Rp 30.000.000",
        "Rp 30.000.000 - Rp 40.000.000",
        "Above Rp 40.000.000",
    ],
    ordered=True,
)


def get_membership_code(series):
    """Get membership code."""
    membership_code = pd.Series(series).str.extract("(\[.+\])")
    membership_code = (
        membership_code.iloc[:, 0]  # convert DF to series
        .str.replace("[", "", regex=False)
        .str.replace("]", "", regex=False)
        .str.replace(".", " ", regex=False)
        .str.replace("(\d+$)", "", regex=True)
        .str.strip()
    )
    return membership_code


def get_membership_duration(series):
    """Get membership duration."""
    membership_code = pd.Series(series).str.extract("(\[.+\])")
    membership_duration = (
        membership_code.iloc[:, 0]  # convert DF to series
        .str.replace("[", "", regex=False)
        .str.replace("]", "", regex=False)
        .str.replace(".", " ", regex=False)
        .str.extract("(\d+)")  # extract digit
    )
    return membership_duration


def is_active(
    df: pd.DataFrame,
    start_date_col: pd.Timestamp,
    end_date_col: pd.Timestamp,
    lower_bound: str,
):
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

    lower_bound = pd.to_datetime(lower_bound)
    upper_bound = lower_bound + pd.offsets.MonthEnd(0)

    conditions = (
        ((df[start_date_col] <= lower_bound) & (df[end_date_col] >= upper_bound)),
        (
            (df[start_date_col] <= lower_bound)
            & (df[end_date_col] <= upper_bound)
            & (df[end_date_col] >= lower_bound)
        ),
        (
            (df[start_date_col] >= lower_bound)
            & (df[start_date_col] <= upper_bound)
            & (df[end_date_col] >= upper_bound)
        ),
        ((df[start_date_col] >= lower_bound) & (df[end_date_col] <= upper_bound)),
        True,
    )
    choices = [True, True, True, True, False]
    return np.select(conditions, choices, default=False)


def clean_center(df_: pd.DataFrame) -> pd.Series:
    """Get center.

    :param pd.DataFrame df_: DF.
    :return pd.Series: Center.
    """

    conditions = [
        df_["is_cpt"] == True, 
        df_["core_product"] == "Go", 
        True,
    ]
    choices = [
        "Corporate",
        "Online Center",
        df_["center"].str.upper().map(center_map),
    ]
    center = np.select(conditions, choices, "ERROR")
    assert (center == "ERROR").sum() == 0, "Some centers are unmapped"
    return center


def clean_area(df_: pd.DataFrame) -> pd.Series:
    """Get area from center.

    :param pd.DataFrame df_: DF.
    :return pd.Series: area.
    """

    conditions = [
        df_["center"].isna(),
        df_["center"] == "Online Center", 
        df_["center"] == "Corporate", 
        df_["center"].isin(jkt_1),
        df_["center"].isin(jkt_2),
        df_["center"].isin(jkt_3),
        df_["center"].isin(bdg),
        df_["center"].isin(sby),
        df_["center"].isin([
            "NST", 
            "HO", 
            "ID",
        ]),
    ]
    choices = [
        np.nan, 
        "Online Center", 
        "Corporate", 
        "JKT 1",
        "JKT 2",
        "JKT 3",
        "BDG",
        "SBY",
        "Other",
    ]
    area = np.select(conditions, choices, default="ERROR")
    assert (area == "ERROR").sum() == 0, "Some centers are unmapped to area"
    return area