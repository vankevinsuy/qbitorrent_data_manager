import time
from handlers.anime_handler import AnimeWatcher
from handlers.movie_handler import MovieWatcher
from handlers.animated_movie_handler import AnimatedMovieWatcher


anime_watcher = AnimeWatcher()
anime_watcher.run()

movie_watcher = MovieWatcher()
movie_watcher.run()

animated_movie_watcher = AnimatedMovieWatcher()
animated_movie_watcher.run()

try:
    while True:
        time.sleep(300)
except:
    print("Observer Stopped")