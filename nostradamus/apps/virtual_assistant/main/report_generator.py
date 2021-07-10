import os
from typing import Optional

from pandas import DataFrame, ExcelWriter
from xlsxwriter.workbook import Format
from datetime import datetime
from pathlib import Path

from apps.extractor.main.connector import get_issues, get_issue_count

SHEET_INDENT = 3
SHEET_FONT_SIZE = 14

REPORT_FIELDS = [
    "Project",
    "Key",
    "Status",
    "Priority",
    "Created",
    "Reporter",
    "Assignee",
]

TYPES_MAPPING = {"created": "date", "project": "drop-down"}


def make_report(
    created_issues: DataFrame, resolved_issues: DataFrame, date: str
) -> dict:
    """Creates status report.

    Parameters
    ----------
    created_issues:
        Issues created on specific date.
    resolved_issues:
        Issues resolved on specific date.
    date:
        Report date.

    Returns
    -------
        Report info.
    """
    file_path = make_report_path(date)
    filename = datetime.strptime(date, "%Y-%m-%dT%H:%M:%S.%f%z").strftime(
        "%Y-%m-%d"
    )

    create_report_file(created_issues, resolved_issues, filename, file_path)

    filename = f"{filename}.xlsx"

    return {
        "size": get_file_size(file_path),
        "filename": filename,
        "format": "xlsx",
        "link": make_report_link(filename),
    }


def build_report_filters(
    field: str, values: tuple, f_type: str, exact_match: bool
) -> list:
    """Creates filters for pymongo query.

    Parameters
    ----------
    field:
        Field to filter by.
    values:
        Field's values.
    f_type:
        Type Field.
    exact_match:
        Filtration option.

    Returns
    -------
        Filters.
    """
    filters = [
        {
            "name": field,
            "type": f_type,
            "current_value": values,
            "exact_match": exact_match,
        }
    ]

    return filters


def make_report_path(date: str) -> str:
    """Creates path for generated report.

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

    return f"{dir_path.joinpath(date.strftime('%Y-%m-%d'))}.xlsx"


def get_report_dir():
    """Creates reports folder if it haven't been create yet.

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
    """Requests file size.

    Parameters
    ----------
    file_path:
        Path to a file.

    Returns
    -------
        File size.
    """

    def _convert_bytes(size: float) -> str:
        """Converts file sizes.

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
    """Generates link to report downloading.

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


def get_issues_for_report(fields, filters) -> DataFrame:
    """Query database for issues which will be written to a report.

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


def create_report_file(
    created_issues: DataFrame,
    resolved_issues: DataFrame,
    filename: str,
    file_path: str,
) -> None:
    """Create report file.

    Parameters
    ----------
    created_issues:
        Issues created on specific date.
    resolved_issues:
        Issues resolved on specific date.
    filename:
        Sheet name.
    file_path:
        File path.
    """
    with ExcelWriter(file_path, engine="xlsxwriter") as writer:
        row = 0

        text_style = writer.book.add_format({"bold": True})
        text_style.set_font_size(SHEET_FONT_SIZE)

        if not writer.book.get_worksheet_by_name(filename):
            sheet = writer.book.add_worksheet(filename)
            writer.sheets.update({filename: sheet})

        row += write_report_dataframe(
            df=created_issues,
            writer=writer,
            sheet_name=filename,
            header="Created",
            text_style=text_style,
            row_number=row,
        )
        row += write_report_dataframe(
            df=resolved_issues,
            writer=writer,
            sheet_name=filename,
            header="Resolved",
            text_style=text_style,
            row_number=row,
        )

        text_style = writer.book.add_format({"bold": True, "border": 1})
        sheet.write_column(
            row,
            0,
            ["Total", "Created", "Resolved"],
            text_style,
        )
        sheet.write_column(
            row,
            1,
            [get_issue_count(), len(created_issues), len(resolved_issues)],
        )


def write_report_dataframe(
    df: DataFrame,
    writer: ExcelWriter,
    sheet_name: str,
    header: str,
    text_style: Format,
    row_number: int,
) -> int:
    """Record dataframe.

    Parameters
    ----------
    df:
        Dataframe.
    writer:
        Object performing excel read/write ops.
    sheet_name:
        Sheet name.
    header:
        Table header.
    text_style:
        Style of table header.
    row_number:
        Row number.

    Returns
    -------
        Number of written rows.
    """
    if not df.empty:
        writer.sheets[sheet_name].write(row_number, 0, header, text_style)
        df.to_excel(
            writer,
            sheet_name=sheet_name,
            index=False,
            startrow=row_number + 1,
        )

        return len(df) + SHEET_INDENT

    return 0


def parse_field(name: str, value: Optional) -> dict:
    """Creates filtration payload.

    Parameters
    ----------
    name:
        Field to be filtrated.
    value:
        Value to filter by.

    Returns
    -------
        Filters payload.
    """
    return {
        "field": name.capitalize(),
        "exact_match": False,
        "values": value,
        "f_type": TYPES_MAPPING[name],
    }
