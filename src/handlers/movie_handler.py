import os
from pathlib import Path
from watchdog.events import FileSystemEvent, PatternMatchingEventHandler
from watchdog.observers import Observer
from sorting.movie import manage_movie
from logging_config import logger


class MovieHandler(PatternMatchingEventHandler):
    def __init__(self, patterns=['*.mp4', '*.mkv'], ignore_patterns=None, ignore_directories=True, case_sensitive=False):
        """
        Initializes the MovieHandler class with the specified patterns, ignore patterns, ignore directories, and case sensitivity settings.
        
        Args:
            patterns (list, optional): A list of file patterns to match, such as '*.mp4' and '*.mkv'. Defaults to ['*.mp4', '*.mkv'].
            ignore_patterns (list, optional): A list of file patterns to ignore. Defaults to None.
            ignore_directories (bool, optional): Whether to ignore directories when matching files. Defaults to True.
            case_sensitive (bool, optional): Whether the file matching should be case sensitive. Defaults to False.
        """
        super().__init__(patterns, ignore_patterns, ignore_directories, case_sensitive)

    def on_created(self, event: FileSystemEvent) -> None:
        """
        Handles the creation of new movie files by triggering the `manage_movie` function.
        
        This function is called whenever a new file is detected in the file system. It logs the name of the new movie file and then calls the `manage_movie` function to handle the new file.
        
        Args:
            event (FileSystemEvent): The file system event that triggered this function.
        """
        try:
            src_path = Path(event.src_path)
            logger.info(f"New movie file detected: {src_path.name}")
            manage_movie(str(src_path))
        except Exception as err:
            logger.error(f"Error occurred while handling movie file: {err}")

class MovieWatcher:
    def __init__(self):
        """
        Initializes the MovieHandler class, which is responsible for monitoring a directory for new movie files.
        
        The directory to monitor is specified by the QBITORRENT_MOVIE_PATH environment variable. If this variable is not set, an error is logged and an EnvironmentError is raised.
        """
        self.observer = Observer()
        self.watch_directory = os.getenv("QBITORRENT_MOVIE_PATH")
        if not self.watch_directory:
            logger.error("QBITORRENT_MOVIE_PATH environment variable is not set.")
            raise EnvironmentError("QBITORRENT_MOVIE_PATH environment variable is not set.")


    def run(self):
        """
        Starts the movie file monitoring process by scheduling a `MovieHandler` event handler to watch the specified directory recursively. Logs a message indicating the directory being watched.
        """
        event_handler = MovieHandler()
        self.observer.schedule(event_handler, self.watch_directory, recursive=True)
        self.observer.start()
        logger.info(f"Watching directory: {self.watch_directory}")
