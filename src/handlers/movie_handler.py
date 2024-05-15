import os
from watchdog.events import FileSystemEvent,PatternMatchingEventHandler
from watchdog.observers import Observer


from sorting.movie import manage_movie

class MovieHandler(PatternMatchingEventHandler):
    def __init__(self, patterns=['*.mp4', '*.mkv'], ignore_patterns=None, ignore_directories=True, case_sensitive=False):
        super().__init__(patterns, ignore_patterns, ignore_directories, case_sensitive)
        
    def on_created(self, event: FileSystemEvent) -> None:
        try:
            print(f"new movie : {event.src_path}")
            manage_movie(event.src_path)
        except Exception as err:
            print(err)
        
class MovieWatcher:
	def __init__(self):
		self.observer = Observer()
		self.watchDirectory = os.getenv("QBITORRENT_MOVIE_PATH")

	def run(self):
		event_handler = MovieHandler()
		self.observer.schedule(event_handler, self.watchDirectory, recursive = True)
		self.observer.start()