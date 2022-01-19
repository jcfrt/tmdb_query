import unittest
import tmdb_client.movie

MOVIE_NAME = "The Matrix"
MOVIE_ID = 603
TV_NAME = "Peaky Blinders"
TV_ID = 60574


class MovieTestCase(unittest.TestCase):
  def test_movie_details(self):
    movie = tmdb_client.movie.Movie(MOVIE_ID)
    movie.details()
    assert hasattr(movie, "title")
    assert movie.title == MOVIE_NAME
  
  def test_movie_credits(self):
    movie = tmdb_client.movie.Movie(MOVIE_ID)
    movie.credits()
    assert hasattr(movie, "cast")


class TVTestCase(unittest.TestCase):
  def test_tv_details(self):
    tv = tmdb_client.movie.TV(TV_ID)
    tv.details()
    assert hasattr(tv, "name")
    assert tv.name == TV_NAME
  
  def test_tv_credits(self):
    tv = tmdb_client.movie.TV(TV_ID)
    tv.credits()
    assert hasattr(tv, "cast")
