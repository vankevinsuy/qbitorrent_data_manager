import os
import shutil
from pathlib import Path
from typing import Optional


ANIMATED_MOVIE_PATH = os.getenv("QBITORRENT_ANIMATED_MOVIE_PATH")
ANIMATED_MOVIE_RELOCATE_PATH = os.getenv("PLEX_ANIMATED_MOVIE_PATH")

def animated_move_movie(animated_movie_path: str) -> None:
    """
    Move an animated movie file to the specified destination path.

    Args:
        animated_movie_path (str): The path of the animated movie file.
    """
    if not ANIMATED_MOVIE_PATH or not ANIMATED_MOVIE_RELOCATE_PATH:
        raise ValueError("Environment variables not set correctly.")

    original_path = Path(animated_movie_path)
    destination_path = Path(ANIMATED_MOVIE_RELOCATE_PATH, original_path.name)
    
    original_path.chmod(0o744)

    os.makedirs(ANIMATED_MOVIE_RELOCATE_PATH, exist_ok=True)
    shutil.move(str(original_path), str(destination_path))


def manage_animated_movie(movie_path: str) -> None:
    """
    Manage an animated movie file by moving it to the specified destination path.

    Args:
        movie_path (str): The path of the animated movie file.
    """
    animated_move_movie(movie_path)
if __name__=='__main__':
    manage_animated_movie()