from typing import Dict
from .tmdb import TMDB


class Search(TMDB):
  """
  Representation of the search API interface.
  Docs @ https://developers.themoviedb.org/3/search
  """
  BASE_PATH = "search"
  SUB_PATH = {
    "movie": ("/movie", "GET"),
    "person": ("/person", "GET")
  }

  def movie(self, **kwargs) -> Dict:
    """
    Search for movies.
    The "query" argument will be URI-encoded.
    Docs @ https://developers.themoviedb.org/3/search/search-movies

    Kwargs:
      language: str (optional).
      query: str (required).
      page: int (optional).
      include_adult: bool (optional).
      region: str (optional).
      year: int (optional).
      primary_release_year: int (optional).
    Returns:
      A JSON response as a dict.
    """
    if "query" not in kwargs.keys():
      raise Exception(f"Missing \"query\" parameter.")
    return self._get("movie", **kwargs)

  def person(self, **kwargs) -> Dict:
    """
    Search for people.
    The "query" argument will be URI-encoded.
    Docs @ https://developers.themoviedb.org/3/search/search-people

    Kwargs:
      language: str (optional).
      query: str (required).
      page: int (optional).
      include_adult: bool (optional).
      region: str (optional).
    Returns:
      A JSON response as a dict.
    """
    if "query" not in kwargs.keys():
      raise Exception(f"Missing \"query\" parameter.")
    return self._get("person", **kwargs)


class Discover(TMDB):
  """
  Representation of the discover API interface.
  Docs @ https://developers.themoviedb.org/3/discover
  """

  BASE_PATH = "discover"
  SUB_PATH = {
    "movie": ("/movie", "GET"),
    "tv": ("/tv", "GET")
  }

  def movie(self, **kwargs) -> Dict:
    """
    Discover movies by different types of data like average rating, number of
    votes, genres and certifications.
    Docs @ https://developers.themoviedb.org/3/discover/movie-discover
    Kwargs:
      See documentation above.
    Returns:
      A JSON response as a dict.
    """
    return self._get("movie", **kwargs)

  def tv(self, **kwargs) -> Dict:
    """
    Docs @ https://developers.themoviedb.org/3/discover/tv-discover
    Kwargs:
      See documentation above.
    Returns
      A JSON response as a dict.
    """
    return self._get("tv", **kwargs)
