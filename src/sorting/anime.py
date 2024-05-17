from dataclasses import dataclass
import os
from pathlib import Path
import re
import shutil
import os


ANIME_PATH = os.getenv("QBITORRENT_ANIME_PATH")
ANIME_RELOCATE_PATH = os.getenv("PLEX_ANIME_PATH")

SUBBER_PATTERN = r"^(\[.*?\])"

PATTERNS = {
    "SubsPlease": {
        "no_season_pattern": r"^\[.*?\]\s(.+)\s-\s(\d+)\s\(\d+p\)\s\[.*?\]\W\w+$",
        "with_season_pattern": r"^\[.*?\]\s(.+)(S\d+)\s-\s(\d+)\s\(\d+p\)\s\[.*?\]\W\w+$"
    },
    "NeoLX": {
        "no_season_pattern": r"^(\[.*?\])\s(.+)\s\[.*?\]\W\w+$",
        "with_season_pattern": r"^(\[.*?\])\s(.+)(S\d+)E(\d+)\s\[.*?\]\W\w+$"
    },
}


@dataclass
class Anime:
    original_path:Path
    title:str
    episode:int
    extension:str
    season:int = 1

def extract_subber(filename:str)->str:
    try:
        subber = re.search(SUBBER_PATTERN, filename)
        if subber:
            subber = subber.group(0).replace('[', '').replace(']', '')
            if subber in PATTERNS.keys():
                return subber
            else:
                raise ValueError(f"Subber {subber} not in PATTERNS")
        else:
            raise ValueError(f"Subber not found {filename}")
    except Exception as err:
        raise Exception(err)

def extract_title(filename:str)->str:
    subber = extract_subber(filename)
    pattern_with_season = PATTERNS[subber]['with_season_pattern']
    pattern_no_season = PATTERNS[subber]['no_season_pattern']
    match_season = re.search(pattern_with_season, filename)
    match_no_season = re.search(pattern_no_season, filename)
    
    if match_season:
        return match_season.group(1).strip()
    if match_no_season:
        return match_no_season.group(1).strip()
    
    return filename.strip()

def extract_episode(filename:str)->int:
    subber = extract_subber(filename)
    pattern_with_season = PATTERNS[subber]['with_season_pattern']
    pattern_no_season = PATTERNS[subber]['no_season_pattern']
    match_season = re.search(pattern_with_season, filename)
    match_no_season = re.search(pattern_no_season, filename)
        
    if match_season:
        return int(match_season.group(3))
    if match_no_season:
        return int(match_no_season.group(2))
    
def extract_season(filename:str)->int:
    subber = extract_subber(filename)
    pattern = PATTERNS[subber]['with_season_pattern']
    match_season = re.search(pattern, filename)
    
    if match_season:
        return int(match_season.group(3).strip().replace('S', ''))

def has_season(filename:str)->bool:
    filename = filename.strip()
    subber = extract_subber(filename)
    pattern = PATTERNS[subber]['with_season_pattern']
    match = re.search(pattern, filename)
    if match:
        return True
    else:
        return False
    
def verify_no_season(filename:str)->bool:
    filename = filename.strip()
    subber = extract_subber(filename)
    pattern = PATTERNS[subber]['no_season_pattern']
    match = re.search(pattern, filename)
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
        try:
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
        except Exception as err:
            print(err)
        
if __name__=='__main__':
    manage_anime()