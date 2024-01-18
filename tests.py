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
    ), "There are unmapped centers. Map this inside modules/center_map."


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
    assert not unmapped, "Some membership are not mapped."