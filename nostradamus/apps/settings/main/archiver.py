import os
import pickle

from pathlib import Path
from typing import Optional
from zipfile import ZipFile

from django.db.models import Model

from apps.analysis_and_training.main.common import get_user_dir
from utils.const import TRAINING_SETTINGS_FILENAME


def get_archive_path(instance: Model) -> Path:
    """ Creates an absolute path to user's archive.

    Parameters:
    ----------
    instance:
        Instance of User or Team model.

    Returns:
    ----------
        Path to user's archive.
    """
    user_dir = get_user_dir(instance)
    archive_path = user_dir.joinpath("archive").joinpath("current.zip")

    return archive_path


def read_from_archive(conf_path: Path, filename: str) -> Optional:
    """ Reads training settings.

    Parameters:
    ----------
    conf_path:
        Absolute path to an archive.
    file_name:
        Name of a file to be read from an archive.

    Returns:
    ----------
        Content of the read file.
    """
    with ZipFile(conf_path, "r") as archive:
        with archive.open(filename, "r") as settings:

            # training_settings is BufferedIOBase instance,
            # so use additional read() method here to get bytes object.
            return pickle.loads(settings.read())


def update_training_config(conf_path: str, settings: bytes) -> None:
    """ Updates user's training settings in archive.

    Parameters:
    ----------
    conf_path:
        Absolute path to archive.
    settings:
        Updated user settings.
    """
    old_path = Path(conf_path)
    old_archive = Path(old_path.parent, "old.zip")
    old_path.rename(old_archive)

    # To update one file in archive need to create new archive
    with ZipFile(old_archive, "r") as old_archive_:
        with ZipFile(conf_path, "w") as new_archive:
            for file in old_archive_.filelist:
                if file.filename != TRAINING_SETTINGS_FILENAME:
                    new_archive.writestr(
                        file, old_archive_.read(file.filename)
                    )
                else:
                    new_archive.writestr(TRAINING_SETTINGS_FILENAME, settings)

    os.remove(old_archive)


def init_archive(instance: Model) -> None:
    """ Creates an archive with default training settings.

    Parameters:
    ----------
    instance:
        Instance of User or Team model.
    """
    from apps.settings.main.common import init_training_settings

    path = get_archive_path(instance)
    with ZipFile(path, "w") as archive:
        training_settings = init_training_settings()
        archive.writestr(TRAINING_SETTINGS_FILENAME, training_settings)


def is_file_in_archive(archive_path: str, file_name: str) -> bool:
    """ Checks whether a file is in an archive.

    Parameters:
    ----------
    archive_path:
        Absolute path to an archive;
    file_name:
        file name.
    
    Returns:
    ----------
        True if the file is in an archive, otherwise False.
    """
    with ZipFile(archive_path, "r") as archive:
        return True if file_name in archive.namelist() else False


def delete_training_data(archive_path: str) -> None:
    """ Deletes training data from archive.

    Parameters:
    ----------
    archive_path:
        Path to archive.
    """
    old_path = Path(archive_path)
    old_archive = Path(old_path.parent, "old.zip")
    old_path.rename(old_archive)

    # To update one file in archive need to create new archive
    with ZipFile(old_archive, "r") as old_archive_:
        with ZipFile(archive_path, "w") as new_archive:
            for file in old_archive_.filelist:
                if file.filename == TRAINING_SETTINGS_FILENAME:
                    new_archive.writestr(
                        file, old_archive_.read(file.filename)
                    )

    os.remove(old_archive)
