from pathlib import Path

import numpy as np
import pandas as pd

import config


def test_all_centers_mapped(df_ori):
    center_in_df = df_ori["Partner/Branch/Display Name"].unique()

    unmapped = []
    for c in center_in_df:
        if isinstance(c, str) and c.upper() not in config.center_map.keys():
            unmapped.append(c)
    assert (
        not unmapped
    ), f"There are unmapped centers: {unmapped}. Map this inside modules/center_map."


def test_all_centers_are_filled(df_clean):
    """
    All centers should be filled with no blank.
    """

    from itertools import chain

    centers_nested = list(config.map_areas.values())
    centers = list(chain(*centers_nested))

    unmapped = set(df_clean["center"].unique()) - set(centers)
    assert (
        not unmapped
    ), f"test_all_centers_are_filled failed, {unmapped} is incorrectly mapped"


def test_all_areas_are_filled(df_clean):
    """
    All areas should be filled with no blank.
    """
    unmapped = set(df_clean["area"].unique()) - set(config.map_areas.keys())
    assert (
        not unmapped
    ), f"test_all_areas_are_filled failed, {unmapped} is incorrectly mapped"


def test_all_memberships_are_filled(df_clean):
    """
    All memberships should be filled with no blank.
    """
    membership_in_df = sorted(
        [c for c in df_clean["core_product"].unique() if isinstance(c, str)]
    )
    assert membership_in_df == [
        "Deluxe",
        "Go",
        "VIP",
    ], "test_all_memberships_are_filled failed"


def test_all_membership_mapped(df_clean):
    # assert that all membership codes has been accounted
    codes = df_clean["membership_code"].unique()
    maps = pd.read_excel(Path("input/membership_mapping.xlsx"))[
        "membership_code"
    ].unique()

    unmapped = []
    for code in codes:
        if code not in maps:
            if code == np.NaN:
                continue
            unmapped.append(code)
    assert not unmapped, f"Some membership are not mapped: {unmapped}. Map them in input/membership_mapping.xlsx"


def test_cpt_is_flagged(df_clean):
    wrong = (
        df_clean.loc[
            df_clean["product"].str.lower().str.contains("cpt|corporate|corp"), "is_cpt"
        ]
        != True
    ).sum()
    assert not wrong, "some cpt members are not correctly flagged"


def test_cpt_in_cpt_center(df_clean):
    assert not (
        df_clean.loc[df_clean["is_cpt"] == True, "center"] != "Corporate"
    ).sum(), "some cpt members are registered outside cpt center"


def test_cpt_in_cpt_area(df_clean):
    assert not (
        df_clean.loc[df_clean["is_cpt"] == True, "area"] != "Corporate"
    ).sum(), "some cpt members are registered outside cpt area"


def test_noncpt_in_noncpt_center(df_clean):
    assert not (
        df_clean.loc[df_clean["is_cpt"] != True, "center"] == "Corporate"
    ).sum(), "some noncpt members are registered in cpt center"


def test_noncpt_in_noncpt_area(df_clean):
    assert not (
        df_clean.loc[df_clean["is_cpt"] != True, "area"] == "Corporate"
    ).sum(), "some noncpt members are registered in cpt area"
