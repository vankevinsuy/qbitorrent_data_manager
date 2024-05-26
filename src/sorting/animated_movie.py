import os
import shutil
from pathlib import Path


ANIMATED_MOVIE_PATH = os.getenv("QBITORRENT_ANIMATED_MOVIE_PATH")
ANIMATED_MOVIE_RELOCATE_PATH = os.getenv("PLEX_ANIMATED_MOVIE_PATH")

def animated_move_movie(animated_movie_path:str)->None:
    original_path = Path(animated_movie_path)
    destination_path: str = f"{ANIMATED_MOVIE_RELOCATE_PATH}/{original_path.name}"
    
    os.makedirs(ANIMATED_MOVIE_RELOCATE_PATH, exist_ok=True)
    
    shutil.move(original_path, destination_path)

def manage_animated_movie(movie_path:str)->None:
    animated_move_movie(movie_path)
        
if __name__=='__main__':
    manage_animated_movie()