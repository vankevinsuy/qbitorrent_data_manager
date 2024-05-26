from logging_config import logger
from flask import Flask, jsonify
from waitress import serve

from handlers.anime_handler import AnimeWatcher
from handlers.movie_handler import MovieWatcher
from handlers.animated_movie_handler import AnimatedMovieWatcher

app = Flask(__name__)

anime_watcher:AnimeWatcher = None
movie_watcher = None
animated_movie_watcher = None

@app.route('/healthcheck', methods=['GET'])
def healthcheck():
    status = {
        'msg':'running'
    }
    return jsonify(status)

def main():
    """
    The main entry point of the AnimeWatcher, MovieWatcher, and AnimatedMovieWatcher applications.
    
    This function starts the three watcher applications and runs them indefinitely until a KeyboardInterrupt (Ctrl+C) is received. The watchers are responsible for monitoring and processing various media types.
    """
    global anime_watcher, movie_watcher, animated_movie_watcher

    logger.info("AnimeWatcher started")
    anime_watcher = AnimeWatcher()
    anime_watcher.run()

    logger.info("MovieWatcher started")
    movie_watcher = MovieWatcher()
    movie_watcher.run()

    logger.info("AnimatedMovieWatcher started")
    animated_movie_watcher = AnimatedMovieWatcher()
    animated_movie_watcher.run()

    try:
        serve(app, host="0.0.0.0", port=1234)
    except KeyboardInterrupt:
        logger.info("Exiting...")
        anime_watcher.stop()
        movie_watcher.stop()
        animated_movie_watcher.stop()

if __name__ == "__main__":
    main()
