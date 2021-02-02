import mimetypes
import os
import shutil

from loguru import logger


def move_file_to_directory(from_file_path: str, file_name: str, to_file_path: str, name_subdir: str):

    target_dir = os.path.join(to_file_path, name_subdir)

    try:
        os.mkdir(target_dir)
    except FileExistsError:
        pass
    try:
        shutil.move(os.path.join(from_file_path, file_name), os.path.join(target_dir, file_name))
    except FileNotFoundError:
        pass


def file_is_valid(file_path: str) -> bool:

    if not os.path.isfile(file_path):
        logger.error('File not found.')
        return False

    mime_type, _ = mimetypes.guess_type(file_path)
    if 'xml' not in mime_type:
        logger.error('File is not xml.')
        return False
    return True
