import pytest
import pandas as pd


@pytest.fixture
def train_df():
    data = [
        [
            1,
            "Defect analysis is cool!",
            "defect,analysis,cool",
            4,
            pd.to_datetime("04-01-2020", utc=True, dayfirst=True),
            1,
            0,
            1,
            "Resolved",
            "High",
        ],
        [
            2,
            "Defect analysis",
            "analysis,pizza,coffee",
            6,
            pd.to_datetime("06-01-2020", utc=True, dayfirst=True),
            0,
            1,
            2,
            "Duplicated",
            "Major",
        ],
        [
            3,
            "Coffee is cool!",
            "defect,analysis,coffee",
            8,
            pd.to_datetime("08-01-2020", utc=True, dayfirst=True),
            1,
            0,
            3,
            "Duplicated",
            "Low",
        ],
    ] * 34
    return pd.DataFrame(
        data=data,
        columns=[
            "Key",
            "Description_tr",
            "Elements",
            "Numbers",
            "Dates",
            "Resolution_Duplicated",
            "Resolution_Fixed",
            "Time to Resolve",
            "Resolution",
            "Priority",
        ],
    )
