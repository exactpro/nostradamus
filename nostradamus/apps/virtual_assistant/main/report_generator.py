import io
import os

from datetime import datetime
from pathlib import Path


from pandas import DataFrame

from apps.extractor.main.connector import get_issues


def make_report(
    new_issues: DataFrame, closed_issues: DataFrame, date: str
) -> dict:
    """ Creates status report.
    
    Parameters
    ----------
    new_issues:
        Issues created on specific date.
    closed_issues:
        Issues resolved on specific date.
    date:
        Report date.

    Returns
    -------
        Report info.
    """

    def _convert_to_string(issues: DataFrame) -> str:
        """ Converts dataframe to string.

        Parameters
        ----------
        issues:
            Dataframe to be converted.

        Returns
        -------
            Stringified Dataframe.
        """
        str_buffer = io.StringIO()

        # Writes issues to in-memory buffer instead of separate file.
        issues.to_csv(str_buffer, index=False)

        return str_buffer.getvalue()

    created_issues = f"New\n{_convert_to_string(new_issues)}\n"
    resolved_issues = f"Closed\n{_convert_to_string(closed_issues)}\n"

    file_path = make_report_path(date)

    with open(file_path, "w") as report:
        report.write(created_issues + resolved_issues)

    size = get_file_size(file_path)

    filename = datetime.strptime(date, "%Y-%m-%dT%H:%M:%S.%f%z")
    filename = f"{filename.strftime('%Y-%m-%d')}.csv"

    return {
        "size": size,
        "filename": filename,
        "format": "csv",
        "link": make_report_link(filename),
    }


def build_report_filters(field: str, period: tuple) -> list:
    """ Creates filters for pymongo query.

    Parameters
    ----------
    field:
        Field to filter by.
    period:
        Period for report generating.

    Returns
    -------
        Filters.
    """
    filters = [
        {
            "name": f"{field}",
            "filtration_type": "date",
            "current_value": period,
            "exact_match": True,
        }
    ]

    return filters


def make_report_path(date: str) -> str:
    """ Creates path for generated report.

    Parameters
    ----------
    date:
        Period for report generating.

    Returns
    -------
        Absolute path to a file.
    """
    dir_path = get_report_dir()
    date = datetime.strptime(date, "%Y-%m-%dT%H:%M:%S.%f%z")

    return f"{dir_path.joinpath(date.strftime('%Y-%m-%d'))}.csv"


def get_report_dir():
    """ Creates reports folder if it haven't been create yet.

    Returns:
    ----------
        Path to reports folder.
    """
    path = Path(__file__).parents[4].joinpath("chatbot").joinpath("reports")

    if os.path.exists(path):
        return path

    path.mkdir(parents=True, exist_ok=True)
    return path


def get_file_size(file_path: str) -> str:
    """ Requests file size.

    Parameters
    ----------
    file_path:
        Path to a file.

    Returns
    -------
        File size.
    """

    def _convert_bytes(size: float) -> str:
        """ Converts file sizes.

        Parameters
        ----------
        size:
            File size in bytes.

        Returns
        -------
            Converted file size.
        """
        for filesize in ["bytes", "KB", "MB", "GB", "TB"]:
            if size < 1024.0:
                return "%3.1f %s" % (size, filesize)
            size /= 1024.0

    info = os.stat(file_path)
    return _convert_bytes(info.st_size)


def make_report_link(filename: str) -> str:
    """ Generates link to report downloading.

    Parameters
    ----------
    filename:
        Report filename.

    Returns
    -------
        Link to report.
    """
    hostname = f"{os.environ.get('SERVER_NAME', default='127.0.0.1')}/api"
    domain = "https://" if "nostradamus" in hostname else "http://"
    path = "/virtual_assistant/reports/"

    return domain + hostname + path + filename


def get_datetime_range(date: str) -> tuple:
    """ Makes one day period by received date.

    Parameters
    ----------
    date:
        Date for report generating.

    Returns
    -------
        Datetime range.
    """
    date = datetime.strptime(date, "%Y-%m-%d")

    from_date = date.strftime("%Y-%m-%dT%H:%M:%S.%f%z") + "Z"
    to_date = (
        date.replace(hour=23, minute=59, second=59).strftime(
            "%Y-%m-%dT%H:%M:%S.%f%z"
        )
        + "Z"
    )

    return from_date, to_date


def get_issues_for_report(fields, filters):
    """ Query database for issues which will be written to a report.

    Parameters
    ----------
    fields:
        Issue fields.
    filters:
        Filters to be applied.

    Returns
    -------
        Issues.
    """
    issues = DataFrame.from_records(get_issues(fields=fields, filters=filters))

    issues = issues.reindex(fields, axis=1)

    return issues
