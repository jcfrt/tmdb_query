from typing import Dict
from .tmdb import TMDB


class Person(TMDB):
  """
  Represent TMDB's person API interface.
  Documentation @ https://developers.themoviedb.org/3/people
  """
  
  BASE_PATH = "person"
  SUB_PATH = {
    "details": ("/{id}", "GET"),
    "combined_credits": ("/{id}/combined_credits", "GET"),
    "movie_credits": ("/{id}/movie_credits", "GET"),
    "tv_credits": ("/{id}/tv_credits", "GET"),
  }

  def __init__(self, id=None) -> None:
    super().__init__()
    self.id = id

  def details(self, **kwargs) -> Dict:
    """
    Get the primary person details by id.
    Docs @ https://developers.themoviedb.org/3/people/get-person-details

    Kwargs:
      language: str (optional).
      append_to_response: str (optional).
    Returns:
      JSON response as a dict.
    """
    return self._get("details", **kwargs)

  def combined_credits(self, **kwargs) -> Dict:
    """
    Get the movie and TV credits together in a single response.
    Docs @ https://developers.themoviedb.org/3/people/get-person-combined-credits

    Kwargs:
      language: str (optional).
    Return:
      JSON response as a dict.
    """
    return self._get("combined_credits", **kwargs)

  def movie_credits(self, **kwargs) -> Dict:
    """
    Get the movie credits for a person.
    Docs @ https://developers.themoviedb.org/3/people/get-person-movie-credits

    Kwargs:
      language: str (optional).
    Return:
      JSON response as a dict.
    """
    return self._get("movie_credits", **kwargs)
