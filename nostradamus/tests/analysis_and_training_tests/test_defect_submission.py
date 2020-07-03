import datetime
import calendar

from pandas import DataFrame

from apps.analysis_and_training.main.charts import calculate_defect_submission


def is_last_month_day():
    now = datetime.datetime.now()
    last_day = calendar.monthlen(now.year, now.month)
    return now.day == last_day


def test_submission_chart_by_day(dates: DataFrame):
    bugs = dates.set_index("Created")
    bugs.index = bugs.index.strftime("%Y-%m-%d")
    bugs = bugs.to_dict()["Key"]

    bugs_by_months = calculate_defect_submission(dates, "Day")

    bugs = dict((key, bugs[key]) for key in bugs if key in bugs_by_months)

    assert bugs == bugs_by_months


def test_submission_chart_by_week(dates: DataFrame):
    bugs = dates.set_index("Created")
    bugs.index = bugs.index.strftime("%Y-%m-%d")
    bugs = bugs.to_dict()["Key"]

    bugs_by_months = calculate_defect_submission(dates, "Week")

    if datetime.datetime.today().isoweekday() != 7:
        bugs_by_months.popitem()

    bugs = dict((key, bugs[key]) for key in bugs if key in bugs_by_months)

    assert bugs == bugs_by_months


def test_submission_chart_by_month(dates: DataFrame):
    bugs = dates.set_index("Created")
    bugs.index = bugs.index.strftime("%Y-%m-%d")
    bugs = bugs.to_dict()["Key"]

    bugs_by_months = calculate_defect_submission(dates, "Month")

    if not is_last_month_day():
        bugs_by_months.popitem()

    bugs = dict((key, bugs[key]) for key in bugs if key in bugs_by_months)

    assert bugs == bugs_by_months


def test_submission_chart_by_3_months(dates: DataFrame):
    bugs = dates.set_index("Created")
    bugs.index = bugs.index.strftime("%Y-%m-%d")
    bugs = bugs.to_dict()["Key"]

    bugs_by_months = calculate_defect_submission(dates, "3 Months")

    if not is_last_month_day():
        bugs_by_months.popitem()

    bugs = dict((key, bugs[key]) for key in bugs if key in bugs_by_months)

    assert bugs == bugs_by_months


def test_submission_chart_by_6_months(dates: DataFrame):
    bugs = dates.set_index("Created")
    bugs.index = bugs.index.strftime("%Y-%m-%d")
    bugs = bugs.to_dict()["Key"]

    bugs_by_months = calculate_defect_submission(dates, "6 Months")

    if not is_last_month_day():
        bugs_by_months.popitem()

    bugs = dict((key, bugs[key]) for key in bugs if key in bugs_by_months)

    assert bugs == bugs_by_months


def test_submission_chart_by_year(dates: DataFrame):
    bugs = dates.set_index("Created")
    bugs.index = bugs.index.strftime("%Y-%m-%d")
    bugs = bugs.to_dict()["Key"]

    bugs_by_months = calculate_defect_submission(dates, "Year")
    bugs_by_months.popitem()

    bugs = dict((key, bugs[key]) for key in bugs if key in bugs_by_months)

    assert bugs == bugs_by_months
