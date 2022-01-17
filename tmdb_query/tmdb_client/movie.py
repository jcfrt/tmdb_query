from typing import Dict
from .tmdb import TMDB


class Movie(TMDB):
  """
  Represent TMDB's movie API interface.
  Documentation @ https://developers.themoviedb.org/3/movie
  """

  BASE_PATH = "movie"
  SUB_PATH = {
    "details": ("/{id}", "GET"),
    "credits": ("/{id}/credits", "GET"),
  }

  def __init__(self, id = None) -> None:
      super().__init__()
      self.id = id

  def details(self, **kwargs) -> Dict:
    """
    Get the primary information about a movie.
    Docs @ https://developers.themoviedb.org/3/movies/get-movie-details

    Kwargs:
      language: str (optional).
      append_to_response: str (optional).
    Returns:
      JSON response as a dict.
    """
    return self._get("details", **kwargs)

  def credits(self, **kwargs) -> Dict:
    """
    Get the cast and crew for a movie.
    Docs @ https://developers.themoviedb.org/3/movies/get-movie-credits

    Kwargs:
      language: str (optional).
      append_to_response: str (optional).
    Returns:
      JSON response as a dict.
    """
    return self._get("credits", **kwargs)


class TV(TMDB):
  """
  Represent TMDB's tv API interface.
  Documentation @ https://developers.themoviedb.org/3/tv
  """

  BASE_PATH = "tv"
  SUB_PATH = {
    "details": ("/{id}", "GET"),
    "credits": ("/{id}/credits", "GET")
  }

  def __init__(self, id = None) -> None:
      super().__init__()
      self.id = id

  def details(self, **kwargs) -> Dict:
    """
    Get the primary TV show details by id.
    Docs @ https://developers.themoviedb.org/3/tv/get-tv-details

    Kwargs:
      language: str (optional).
      append_to_response: str (optional).
    Returns:
      JSON response as a dict.
    """
    return self._get("details", **kwargs)

  def credits(self, **kwargs) -> Dict:
    """
    Get the credits (cast and crew) that have been added to a TV show.
    Docs @ https://developers.themoviedb.org/3/tv/get-tv-credits

    Kwargs:
      language: str (optional).
    Returns:
      JSON response as a dict.
    """
    return self._get("credits", **kwargs)
