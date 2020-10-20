import os
import zipfile

from pandas import DataFrame, Series
from django.db.models import Model

from utils.const import STOP_WORDS
from itertools import chain
from pathlib import Path

MIN_CLASS_PERCENTAGE = 0.01


def check_bugs_count(issues: DataFrame, required_count: int = 100) -> bool:
    """Checks the number of bugs in the dataset.

    Parameters:
    ----------
    issues:
        Bug reports.
    required_count:
        required count bugs.

    Returns:
    ----------
        True, if the required count of bugs is present in the dataset,
        otherwise it is False.
    """
    return len(issues.index) >= required_count


def unpack_lists(lists: list) -> list:
    """Unpacks two-dimensional lists to one-dimensional.

    Parameters:
    ----------
    lists:
        two-dimensional list.

    Returns:
    ----------
        Unpacked one-dimensional list.
    """
    return list(chain(*lists))


def get_user_dir(instance: Model) -> Path:
    """Creates assets/usr/%id% directory if it haven't been created before.

    Parameters:
    ----------
    instance:
            Instance of User model.

    Returns:
    ----------
        Path to user instance directory.
    """
    usr_path = Path(__file__).parents[3].joinpath("assets").joinpath("usr")
    instance_path = usr_path.joinpath(str(instance.id))

    if os.path.exists(instance_path):
        return instance_path

    instance_path.mkdir(parents=True, exist_ok=True)
    return instance_path


def get_models_dir(instance: Model) -> Path:
    """Creates current.zip archive if it haven't been created before.

    Parameters:
    ----------
    instance:
            Instance of User model.

    Returns:
    ----------
        Path to user/archive/current.zip.
    """
    path = get_user_dir(instance).joinpath("archive").joinpath("current.zip")

    if os.path.exists(path):
        return path

    zip_file = zipfile.ZipFile(path, "w", compression=zipfile.ZIP_DEFLATED)
    zip_file.close()
    return path


def get_team_dir(instance: Model) -> Path:
    """Creates assets/team/%id% directory if it haven't been created before.

    Parameters:
    ----------
    instance:
        Instance of Team model.

    Returns:
    ----------
        Path to team/%id% directory.
    """
    team_path = Path(__file__).parents[3].joinpath("assets").joinpath("team")
    instance_path = team_path.joinpath(str(instance.id))

    if os.path.exists(instance_path):
        return instance_path

    instance_path.mkdir(parents=True, exist_ok=True)
    return instance_path


def init_instance_folders(path: Path) -> None:
    """Creates backup and archive folders in instance directory.

    Parameters:
    ----------
    instance:
        Instance of User or Team model.
    path:
        Path to usr or team directory.
    """
    path.joinpath("archive").mkdir(exist_ok=True)
    path.joinpath("backup").mkdir(exist_ok=True)


def check_required_percentage(series: Series, value: str) -> bool:
    """Checks whether the value represents required percentage
    in handled series.

    Parameters:
    ----------
    series:
        series used for percentage calculations.
    value:
        metric is used for percentage calculations.

    Returns:
    ----------
        True if value percentage is greater than 1% from the whole series
        otherwise False.
    """
    return series[series == value].size / series.size >= MIN_CLASS_PERCENTAGE


def get_assignee_reporter(issues: DataFrame) -> set:
    """Parsing full names from Assignee and Reported series

    Parameters:
    ----------
    issues:
        Bug reports.

    Returns:
    ----------
        Unique names and last names.
    """
    full_names = [
        full_name.lower().split()
        for full_name in issues["Assignee"].tolist()
        + issues["Reporter"].tolist()
    ]

    assignee_reporter = set(unpack_lists(full_names))

    return assignee_reporter


def get_stop_words(issues: DataFrame) -> set:
    """Generates stop words for TfidfVectorizer constructor.

    Parameters:
    ----------
    issues:
        Bug reports.

    Returns:
    ----------
        Unique words which will be ignored.
    """
    assignee_reporter = get_assignee_reporter(issues)

    return STOP_WORDS.union(assignee_reporter)


def save_to_archive(archive_path: Path, file_name: str, content):
    """Saves content to a file and appends it to archive.

    Parameters:
    ----------
    archive_path:
        Path to an archive.
    file_name:
        Name of the file which will be appended to archive.
    content:
        Data to be written to the file.
    """
    with zipfile.ZipFile(archive_path, "a") as file_:
        file_.writestr(file_name, content, compress_type=zipfile.ZIP_DEFLATED)
