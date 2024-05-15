import os
import shutil
from pathlib import Path


MOVIE_PATH = os.getenv("QBITORRENT_MOVIE_PATH")
MOVIE_RELOCATE_PATH = os.getenv("PLEX_MOVIE_PATH")

def move_movie(movie_path:str)->None:
    original_path = Path(movie_path)
    destination_path: str = f"{MOVIE_RELOCATE_PATH}/{original_path.name}"
    
    os.makedirs(MOVIE_RELOCATE_PATH, exist_ok=True)
    
    shutil.move(original_path, destination_path)

def manage_movie(movie_path:str)->None:
    move_movie(movie_path)
        
if __name__=='__main__':
    manage_movie()