from dataclasses import dataclass
import os
from pathlib import Path
import re
import shutil
import os


ANIME_PATH = os.getenv("QBITORRENT_ANIME_PATH")
ANIME_RELOCATE_PATH = os.getenv("PLEX_ANIME_PATH")

NO_SEASON_PATTERN = r"^\[.*?\]\s(.+)\s-\s(\d+)\s\(\d+p\)\s\[.*?\]\W\w+$"
WITH_SEASON_PATTERN = r"^\[.*?\]\s(.+)(S\d+)\s-\s(\d+)\s\(\d+p\)\s\[.*?\]\W\w+$"

@dataclass
class Anime:
    original_path:Path
    title:str
    episode:int
    extension:str
    season:int = 1

def extract_title(filename:str)->str:
    match_season = re.search(WITH_SEASON_PATTERN, filename)
    match_no_season = re.search(NO_SEASON_PATTERN, filename)
    
    if match_season:
        return match_season.group(1).strip()
    if match_no_season:
        return match_no_season.group(1).strip()
    
    return filename.strip()

def extract_episode(filename:str)->int:
    match_season = re.search(WITH_SEASON_PATTERN, filename)
    match_no_season = re.search(NO_SEASON_PATTERN, filename)
        
    if match_season:
        return int(match_season.group(3))
    if match_no_season:
        return int(match_no_season.group(2))
    
def extract_season(filename:str)->int:
    match_season = re.search(WITH_SEASON_PATTERN, filename)
    
    if match_season:
        return match_season.group(2).strip().replace('S', '')

def has_season(filename:str)->bool:
    filename = filename.strip()
    match = re.search(WITH_SEASON_PATTERN, filename)
    if match:
        return True
    else:
        return False
    
def verify_no_season(filename:str)->bool:
    filename = filename.strip()
    match = re.search(NO_SEASON_PATTERN, filename)
    if match:
        return True
    else:
        return False

def move_anime(anime:Anime)->None:
    destination_folder: str = f"{ANIME_RELOCATE_PATH}/{anime.title}/season_{anime.season}/"
    destination_path: str = f"{destination_folder}/{anime.original_path.name}"
    
    os.makedirs(os.path.dirname(destination_folder), exist_ok=True)

    shutil.move(str(anime.original_path), destination_path)

def manage_anime()->None:
    for file in os.listdir(ANIME_PATH):
        anime_file = Path(f"{ANIME_PATH}/{file}")
        if has_season(file):
            anime = Anime(
                original_path=anime_file,
                title=extract_title(file),
                episode=extract_episode(file),
                extension=anime_file.suffix,
                season=extract_season(file),
            )
        else:
            if verify_no_season(file):
                anime = Anime(
                    original_path=anime_file,
                    title=extract_title(file),
                    episode=extract_episode(file),
                    extension=anime_file.suffix,
                )
                
        move_anime(anime)
        
if __name__=='__main__':
    manage_anime()