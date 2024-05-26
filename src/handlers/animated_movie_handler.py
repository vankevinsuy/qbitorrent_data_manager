import os
from pathlib import Path
from watchdog.events import FileSystemEvent, PatternMatchingEventHandler
from watchdog.observers import Observer
from sorting.animated_movie import manage_animated_movie
from logging_config import logger


class AnimatedMovieHandler(PatternMatchingEventHandler):
    def __init__(self, patterns=['*.mp4', '*.mkv'], ignore_patterns=None, ignore_directories=True, case_sensitive=False):
        """
        Initializes the AnimatedMovieHandler class with the specified patterns, ignore patterns, ignore directories, and case sensitivity settings.
        
        Args:
            patterns (list, optional): A list of file patterns to match. Defaults to ['*.mp4', '*.mkv'].
            ignore_patterns (list, optional): A list of file patterns to ignore. Defaults to None.
            ignore_directories (bool, optional): Whether to ignore directories. Defaults to True.
            case_sensitive (bool, optional): Whether the file matching should be case sensitive. Defaults to False.
        """
        super().__init__(patterns, ignore_patterns, ignore_directories, case_sensitive)

    def on_created(self, event: FileSystemEvent) -> None:
        """
        Handles the creation of new animated movie files by triggering the management of the movie.
        
        Args:
            event (FileSystemEvent): The file system event that triggered this handler.
        
        Raises:
            Exception: If there is an error processing the animated movie.
        """
        try:
            src_path = Path(event.src_path)
            logger.info(f"New animated movie detected: {src_path}")
            manage_animated_movie(src_path)
        except Exception as err:
            logger.error(f"Error processing animated movie: {src_path}", exc_info=True)

class AnimatedMovieWatcher:
    def __init__(self):
        """
        Initializes the AnimatedMovieHandler class, which is responsible for monitoring a directory for new animated movie files.
        
        The class requires the QBITORRENT_ANIMATED_MOVIE_PATH environment variable to be set, which specifies the directory to monitor. If the environment variable is not set, an EnvironmentError is raised.
        """
        self.observer = Observer()
        self.watch_directory = os.getenv("QBITORRENT_ANIMATED_MOVIE_PATH")
        if not self.watch_directory:
            logger.error("QBITORRENT_ANIMATED_MOVIE_PATH environment variable is not set.")
            raise EnvironmentError("QBITORRENT_MOVIE_PATH environment variable is not set.")


    def run(self):
        """
        Starts the file monitoring process for the animated movie handler.
        
        This method schedules the `AnimatedMovieHandler` to watch the directory specified by `self.watch_directory`, and recursively monitors all subdirectories. It then starts the monitoring process.
        
        After starting the monitoring, it logs an informational message indicating the directory being watched.
        """
        event_handler = AnimatedMovieHandler()
        self.observer.schedule(event_handler, self.watch_directory, recursive=True)
        self.observer.start()
        logger.info(f"Watching directory: {self.watch_directory}")
