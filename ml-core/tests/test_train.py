import pandas as pd
import pytest

from training.training import (
    compare_resolutions,
    get_k_neighbors,
    stringify_ttr_intervals,
)

from error_handlers.exceptions import SmallNumberRepresentatives


def test_compare_resolutions_positive(train_df):
    resolutions = ["Duplicated", "Resolved"]
    assert not compare_resolutions(train_df.Resolution, resolutions)


def test_compare_resolutions_positive_2(train_df):
    resolutions = ["Duplicated"]
    assert not compare_resolutions(train_df.Resolution, resolutions)


def test_compare_resolutions_negative(train_df):
    resolutions = ["Duplicated", "Fixed", "Resolved"]
    assert compare_resolutions(train_df.Resolution, resolutions) == set(["Fixed"])


def test_get_k_neighbors_positive(train_df):
    assert get_k_neighbors(train_df["Description_tr"]) == 2


def test_get_k_neighbors_positive_2(train_df):
    len_df = len(train_df)
    test_df = train_df
    for i in range(len_df, len_df + 4):
        test_df.loc[i] = [
            i,
            "test",
            "defect,analysis,coffee",
            8,
            pd.to_datetime("08-01-2020", utc=True, dayfirst=True),
            1,
            0,
            10,
            "Duplicated",
            "Low",
        ]

    assert get_k_neighbors(test_df["Description_tr"]) == 2


def test_get_k_neighbors_negative(train_df):
    test_df = train_df
    test_df.loc[len(train_df)] = [
        len(train_df),
        "test",
        "defect,analysis,coffee",
        8,
        pd.to_datetime("08-01-2020", utc=True, dayfirst=True),
        1,
        0,
        10,
        "Duplicated",
        "Low",
    ]
    with pytest.raises(SmallNumberRepresentatives):
        get_k_neighbors(test_df["Description_tr"])


def test_stringify_ttr_intervals_positive():
    intervals = [
        pd.Interval(0, 4),
        pd.Interval(4, 6),
        pd.Interval(6, 9),
        pd.Interval(9, 10),
    ]
    expected_result = ["0-4", "5-6", "7-9", ">9"]
    assert stringify_ttr_intervals(intervals) == expected_result


def test_stringify_ttr_intervals_negative():
    intervals = [
        pd.Interval(-0.01, 4),
        pd.Interval(4, 6),
        pd.Interval(6, 9),
        pd.Interval(9, 10),
    ]
    expected_result = ["0-4", "5-6", "7-9", ">9"]
    assert stringify_ttr_intervals(intervals) == expected_result
