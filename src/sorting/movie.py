import os
import shutil
from pathlib import Path
from typing import Optional

MOVIE_PATH = os.getenv("QBITORRENT_MOVIE_PATH")
MOVIE_RELOCATE_PATH = os.getenv("PLEX_MOVIE_PATH")


def move_movie(movie_path: str) -> None:
    """
    Move a movie file to the specified destination path.

    Args:
        movie_path (str): The path of the movie file.
    """
    if not MOVIE_PATH or not MOVIE_RELOCATE_PATH:
        raise ValueError("Environment variables not set correctly.")

    original_path = Path(movie_path)
    destination_path = Path(MOVIE_RELOCATE_PATH) / original_path.name

    os.makedirs(MOVIE_RELOCATE_PATH, exist_ok=True)
    shutil.move(str(original_path), str(destination_path))


def manage_movie(movie_path: Optional[str] = None) -> None:
    """
    Manage a movie file by moving it to the specified destination path.

    Args:
        movie_path (Optional[str]): The path of the movie file. If not provided,
            the function will exit without doing anything.
    """
    if movie_path is None:
        return

    move_movie(movie_path)


if __name__ == '__main__':
    # Example usage
    manage_movie()
