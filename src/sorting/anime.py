import os
import re
import shutil
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Optional, Pattern

ANIME_PATH = os.getenv("QBITORRENT_ANIME_PATH")
ANIME_RELOCATE_PATH = os.getenv("PLEX_ANIME_PATH")

SUBBER_PATTERN = re.compile(r"^(\[.*?\])")
NOSUBBER_PATTERN = re.compile(r"^(.+).S(\d+)E(\d+)")

SUBBER_POSITION = 0

PATTERNS: Dict[str, Dict[str, Optional[Pattern]]] = {
    "SubsPlease": {
        "no_season_pattern": re.compile(r"^\[.*?\]\s(.+)\s-\s(\d+)\s\(\d+p\)\s\[.*?\]\W\w+$"),
        "with_season_pattern": re.compile(r"^\[.*?\]\s(.+)(S\d+)\s-\s(\d+)\s\(\d+p\)\s\[.*?\]\W\w+$"),
        'title_pos': 1,
        'episode_pos_with_season': 3,
        'episode_pos_no_season': 2,
        'season_pos': 2
    },
    "NeoLX": {
        "no_season_pattern": re.compile(r"^\[.*?\]\s(.+)\s\[.*?\]\W\w+$"),
        "with_season_pattern": re.compile(r"^\[.*?\]\s(.+)(S\d+)E(\d+)\s\[.*?\]\W\w+$"),
        'title_pos': 1,
        'episode_pos_with_season': 3,
        'episode_pos_no_season': None,
        'season_pos': 2
    },
    "Erai-raws":{
        "no_season_pattern": re.compile(r"^(\[.*?\])\s(.+)\s-\s(\d+)"),
        "with_season_pattern": re.compile(r"^(\[.*?\])\s(.+)(\d+)\s-\s(\d+)"),
        'title_pos': 2,
        'episode_pos_with_season': 4,
        'episode_pos_no_season': 3,
        'season_pos': 3
    },
    "NoSubber":{
        "no_season_pattern": re.compile(r""),
        "with_season_pattern": re.compile(r"^(.+).S(\d+)E(\d+)"),
        'title_pos': 1,
        'episode_pos_with_season': 3,
        'episode_pos_no_season': 3,
        'season_pos': 2
    }
}


@dataclass
class Anime:
    """
    Represents an anime file with metadata such as the original path, title, episode, extension, and season.
    
    The `__post_init__` method is called after the object is initialized, and it strips any leading or trailing whitespace from the `title` attribute.
    """
    original_path: Path
    title: str
    episode: int
    extension: str
    season: int = 1

    def __post_init__(self):
        self.title = self.title.strip()


def extract_subber(filename: str) -> str:
    """
    Extracts the subber from the given filename.
    
    Args:
        filename (str): The filename to extract the subber from.
    
    Returns:
        str: The subber extracted from the filename.
    
    Raises:
        ValueError: If the subber is not found in the filename or the extracted subber is not in the PATTERNS list.
    """
    match = SUBBER_PATTERN.search(filename)
    if match:
        subber = match.group(SUBBER_POSITION).strip('[]')
        if subber in PATTERNS:
            return subber
        raise ValueError(f"Subber {subber} not in PATTERNS")
    else:
        no_subber_match = NOSUBBER_PATTERN.search(filename)
        if no_subber_match:
            return "NoSubber"
        
    raise ValueError(f"Subber not found {filename}")


def extract_title(filename: str) -> str:
    """
    Extracts the title from a given filename based on the subber's pattern.
    
    Args:
        filename (str): The filename to extract the title from.
    
    Returns:
        str: The extracted title.
    
    Raises:
        ValueError: If no match pattern is found for the title in the filename.
    """
    subber = extract_subber(filename)
    pattern_with_season = PATTERNS[subber]['with_season_pattern']
    pattern_no_season = PATTERNS[subber]['no_season_pattern']
    match_season = pattern_with_season.search(filename)
    match_no_season = pattern_no_season.search(filename)

    if match_season:
        return match_season.group(PATTERNS[subber]['title_pos']).strip()
    if match_no_season:
        return match_no_season.group(PATTERNS[subber]['title_pos']).strip()
    raise ValueError(f"No match pattern for title {filename}")


def extract_episode(filename: str) -> int:
    """
    Extracts the episode number from a given filename based on the subber's pattern.
    
    Args:
        filename (str): The filename to extract the episode number from.
    
    Returns:
        int: The extracted episode number.
    
    Raises:
        ValueError: If no match pattern is found for the episode in the filename.
    """
    subber = extract_subber(filename)
    pattern_with_season = PATTERNS[subber]['with_season_pattern']
    pattern_no_season = PATTERNS[subber]['no_season_pattern']
    match_season = pattern_with_season.search(filename)
    match_no_season = pattern_no_season.search(filename)

    if match_season:
        return int(match_season.group(PATTERNS[subber]['episode_pos_with_season']))
    if match_no_season:
        episode_pos = PATTERNS[subber]['episode_pos_no_season']
        if episode_pos is not None:
            return int(match_no_season.group(episode_pos))
    raise ValueError(f"No match pattern for episode {filename}")


def extract_season(filename: str) -> int:
    """
    Extracts the season number from an anime filename based on the subber's pattern.
    
    Args:
        filename (str): The anime filename to extract the season number from.
    
    Returns:
        int: The extracted season number.
    
    Raises:
        ValueError: If no match pattern is found for the given filename.
    """
    subber = extract_subber(filename)
    pattern = PATTERNS[subber]['with_season_pattern']
    match_season = pattern.search(filename)

    if match_season:
        return int(match_season.group(PATTERNS[subber]['season_pos']).strip('S'))
    raise ValueError(f"No match pattern for season {filename}")


def has_season(filename: str) -> bool:
    """
    Checks if the given filename contains a season number.
    
    Args:
        filename (str): The filename to check.
    
    Returns:
        bool: True if the filename contains a season number, False otherwise.
    """
    subber = extract_subber(filename)
    pattern = PATTERNS[subber]['with_season_pattern']
    return bool(pattern.search(filename))


def verify_no_season(filename: str) -> bool:
    """
    Checks if the given filename does not contain a season number.
    
    Args:
        filename (str): The filename to check.
    
    Returns:
        bool: True if the filename does not contain a season number, False otherwise.
    """
    subber = extract_subber(filename)
    pattern = PATTERNS[subber]['with_season_pattern']
    return not bool(pattern.search(filename))


def move_anime(anime: Anime) -> None:
    """
    Moves an anime file to a destination folder based on its title and season.
    
    Args:
        anime (Anime): The anime object containing the information needed to move the file.
    
    Raises:
        OSError: If there is an error creating the destination folder.
    """
    destination_folder = f"{ANIME_RELOCATE_PATH}/{anime.title}/season_{anime.season}/"
    destination_path = f"{destination_folder}/{anime.original_path.name}"

    os.makedirs(os.path.dirname(destination_folder), exist_ok=True)
    shutil.move(str(anime.original_path), destination_path)


def manage_anime() -> None:
    """
    Manages the processing of anime files in the ANIME_PATH directory.
    
    This function iterates through all files in the ANIME_PATH directory, and for each file:
    - Checks if the file has a season number, and if so, creates an Anime object with the title, episode, extension, and season.
    - If the file does not have a season number, it checks if the file can be verified as having no season, and if so, creates an Anime object with the title, episode, and extension.
    - Calls the move_anime function to process the Anime object.
    
    Any exceptions that occur during the processing of a file are caught and printed.
    """
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


if __name__ == '__main__':
    manage_anime()
