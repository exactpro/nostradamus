import datetime

from pandas import DataFrame

from apps.analysis_and_training.main.charts import get_defect_submission


def test_submission_chart_by_day(dates: DataFrame):
    bugs = dates.set_index("Created")
    bugs.index = bugs.index.strftime("%d.%m.%Y")
    bugs = bugs.to_dict()["Key"]

    bugs_by_months = get_defect_submission(dates, "Day")["created_line"]

    bugs = dict((key, bugs[key]) for key in bugs if key in bugs_by_months)

    assert bugs == bugs_by_months


def test_submission_chart_by_week(dates: DataFrame):
    bugs = dates.set_index("Created")
    bugs.index = bugs.index.strftime("%d.%m.%Y")
    bugs = bugs.to_dict()["Key"]

    bugs_by_months = get_defect_submission(dates, "Week")["created_line"]

    if datetime.datetime.today().isoweekday() != 7:
        bugs_by_months.popitem()

    bugs = dict((key, bugs[key]) for key in bugs if key in bugs_by_months)

    assert bugs == bugs_by_months


def test_submission_chart_by_month(dates: DataFrame):
    bugs = dates.set_index("Created")
    bugs.index = bugs.index.strftime("%b %Y")
    bugs = bugs.to_dict()["Key"]

    bugs_by_months = get_defect_submission(dates, "Month")["created_line"]

    bugs = dict((key, bugs[key]) for key in bugs if key in bugs_by_months)

    assert bugs == bugs_by_months


def test_submission_chart_by_3_months(dates: DataFrame):
    bugs = dates.set_index("Created")
    bugs.index = bugs.index.strftime("%b %Y")
    bugs = bugs.to_dict()["Key"]

    bugs_by_months = get_defect_submission(dates, "3 Months")["created_line"]
    bugs_by_months.popitem()

    bugs = dict((key, bugs[key]) for key in bugs if key in bugs_by_months)

    assert bugs == bugs_by_months


def test_submission_chart_by_6_months(dates: DataFrame):
    bugs = dates.set_index("Created")
    bugs.index = bugs.index.strftime("%b %Y")
    bugs = bugs.to_dict()["Key"]

    bugs_by_months = get_defect_submission(dates, "6 Months")["created_line"]
    bugs_by_months.popitem()

    bugs = dict((key, bugs[key]) for key in bugs if key in bugs_by_months)

    assert bugs == bugs_by_months


def test_submission_chart_by_year(dates: DataFrame):
    bugs = dates.set_index("Created")
    bugs.index = bugs.index.strftime("%Y")
    bugs = bugs.to_dict()["Key"]

    bugs_by_months = get_defect_submission(dates, "Year")["created_line"]
    bugs_by_months.popitem()

    bugs = dict((key, bugs[key]) for key in bugs if key in bugs_by_months)

    assert bugs == bugs_by_months


def test_coordinates_equality(dates: DataFrame):
    bugs = dates.set_index("Created")
    bugs.index = bugs.index.strftime("%Y")

    bugs_by_months = get_defect_submission(dates, "Month")

    resolved_line_points = bugs_by_months["resolved_line"].keys()
    created_line_points = bugs_by_months["created_line"].keys()

    assert set(resolved_line_points) == set(created_line_points)
