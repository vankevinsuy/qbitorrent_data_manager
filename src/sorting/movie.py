import os
import shutil


MOVIE_PATH = os.getenv("QBITORRENT_MOVIE_PATH")
MOVIE_RELOCATE_PATH = os.getenv("PLEX_MOVIE_PATH")

def move_movie(movie:str)->None:
    destination_path: str = f"{MOVIE_RELOCATE_PATH}/{movie}"
    
    os.makedirs(MOVIE_RELOCATE_PATH, exist_ok=True)

    shutil.move(f"{MOVIE_PATH}/{movie}", destination_path)


def manage_movie()->None:
    for file in os.listdir(MOVIE_PATH):
        move_movie(file)
        
if __name__=='__main__':
    manage_movie()