import os
from watchdog.events import FileSystemEvent, FileSystemEventHandler
from watchdog.observers import Observer

from sorting.movie import manage_movie

class MovieHandler(FileSystemEventHandler):
	def on_created(self, event: FileSystemEvent) -> None:
		try:
			print(f"new movie : {event.src_path}")
			manage_movie()
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