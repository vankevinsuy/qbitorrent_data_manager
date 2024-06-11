import os
from pathlib import Path
from watchdog.events import FileSystemEvent, PatternMatchingEventHandler
from watchdog.observers import Observer
from sorting.anime import manage_anime
from logging_config import logger

class AnimeHandler(PatternMatchingEventHandler):
    def __init__(self, patterns=['*.mp4', '*.mkv'], ignore_patterns=None, ignore_directories=True, case_sensitive=False):
        """
        Initializes the AnimeHandler class with the specified patterns, ignore patterns, ignore directories, and case sensitivity settings.
        
        Args:
            patterns (list, optional): A list of file patterns to match. Defaults to ['*.mp4', '*.mkv'].
            ignore_patterns (list, optional): A list of file patterns to ignore. Defaults to None.
            ignore_directories (bool, optional): Whether to ignore directories. Defaults to True.
            case_sensitive (bool, optional): Whether the pattern matching should be case sensitive. Defaults to False.
        """
        super().__init__(patterns, ignore_patterns, ignore_directories, case_sensitive)

    def on_created(self, event: FileSystemEvent) -> None:
        """
        Handles the creation of new anime files by calling the `manage_anime()` function.
        
        This function is called whenever a new file is detected in the monitored directory. It logs the name of the new file and then calls the `manage_anime()` function to handle the new file.
        
        Args:
            event (FileSystemEvent): The event object that triggered this function.
        """
        try:
            src_path = Path(event.src_path)
            logger.info(f"New anime file detected: {src_path.name}")
            manage_anime()
        except Exception as err:
            logger.error(f"Error occurred while handling anime file: {err}")

class AnimeWatcher:
    def __init__(self):
        self.observer = Observer()
        self.watch_directory = os.getenv("QBITORRENT_ANIME_PATH")
        if not self.watch_directory:
            logger.error("QBITORRENT_ANIME_PATH environment variable is not set.")
            raise EnvironmentError("QBITORRENT_ANIME_PATH environment variable is not set.")

    def run(self):
        """
        Starts the file monitoring process for the anime download directory.
        
        This method schedules an `AnimeHandler` event handler to monitor the directory specified by `self.watch_directory`. It then starts the file monitoring process using the `observer.start()` method.
        
        The method logs an informational message indicating the directory being watched.
        """
        event_handler = AnimeHandler()
        self.observer.schedule(event_handler, self.watch_directory, recursive=True)
        logger.info(f"Watching directory: {self.watch_directory}")
        self.observer.start()
