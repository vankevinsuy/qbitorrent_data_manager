import os
import time
from watchdog.events import FileSystemEvent, FileSystemEventHandler
from watchdog.observers import Observer

from anime_sorting import manage_anime

class AnimeHandler(FileSystemEventHandler):
    def on_created(self, event: FileSystemEvent) -> None:
        manage_anime()
        
        
class Anime_watcher:
	def __init__(self):
		self.observer = Observer()
		self.watchDirectory = os.getenv("QBITORRENT_ANIME_PATH")

	def run(self):
		event_handler = AnimeHandler()
		self.observer.schedule(event_handler, self.watchDirectory, recursive = True)
		self.observer.start()
		try:
			while True:
				time.sleep(5)
		except:
			self.observer.stop()
			print("Observer Stopped")

		self.observer.join()