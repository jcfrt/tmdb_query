from typing import Iterable, List, Dict, Any, AbstractSet
import logging
from tmdb_client.person import Person
from tmdb_client.movie import Movie

log = logging.getLogger(__name__)


def add_all_to(str_list: List, obj: object) -> None:
  """
  Add each element in the .results attribute from obj to the list pointed
  at by str_list.
  Args:
    str_list: list. The mutable list to append to.
    obj: object. The object from which to read the "results" attribute.
  Returns:
    None.
  
  >>> class Object(object):
  >>>   pass
  >>> obj = object()
  >>> setattr(obj, "results", [{"title": "a_title"}, {"title", "another_title"}])
  >>> _list = []
  >>> add_all_to(_list, obj)
  >>> assert "a_title" in _list
  >>> assert "another_title" in _list 
  """
  for el in getattr(obj, "results", []):
    str_list.append(el.get("title"))


MEDIA_TITLE_KEYS = ["original_name", "name", "original_title"]

def get_first_known_key(mapping: Dict, known_keys: Iterable = MEDIA_TITLE_KEYS) -> Any:
  """
  Retrieve the first value found among entry's keys.
  Args:
    mapping: dict. The mapping to traverse.
    known_keys: iterable. Keys to look for in mapping.
  Returns:
    The value of the first key in known_keys that does not evaluate to false.
    If no key is found in entry, returns None.
  
  >>> _dict = {"a_title": "foo", "name": "bar", "a_key": "a_value"}
  >>> assert get_first_known_key(_dict, ("name",)) == "bar"
  """
  for key in known_keys:
    if value := mapping.get(key):
      return value
  return None


def is_actor(result: Dict) -> bool:
  """
  Args:
    results: dict. A result dictionary as output by the Search class.
  Returns:
    True if the "known_for_department" key equals "Acting", otherwise False.
  """
  if known_for := result.get("known_for_department"):
    if known_for == "Acting":
      return True
    return False
  elif _id := result.get("id"):
    # Fallback to getting details if we have the id at least:
    person = Person(_id)
    person.details()
    if getattr(person, "known_for_department", "") == "Acting":
      return True
    return False
  raise Exception("Missing known_for_department or id key.")


def get_movie_cast(movie_id: int) -> AbstractSet[int]:
  """
  For a given movie id, return only the cast members that were actors.
  Args:
    movie_id: int. Unique TMDB movie ID.
  Returns:
    A set of unique TMDB actor IDs.
  """
  actor_ids = set()
  movie = Movie(movie_id)
  creds = movie.credits()
  cast = creds.get("cast", [])
  for cast_entry in cast:
    if cast_entry.get("known_for_department", "") == "Acting":
      if actor_id := cast_entry.get("id"):
        log.debug(f"Detected id {actor_id} of {cast_entry.get('name', '')} to actor_ids for movie {movie_id}.")
        actor_ids.add(actor_id)
  return actor_ids


def get_movies_id_for_actor_id(actor_id: int) -> Dict[int, str]:
  """
  For a given actor id, get all movies by id that this actor was part of as cast.
  Args:
    actor_id: str. ID of the actor to look up.
  Returns:
    A dictionary of {movie_id: movie_title}
  """
  movies_map = {}
  actor = Person(actor_id)
  creds = actor.movie_credits()
  cast = creds.get("cast", [])
  for movie in cast:
    movies_map[int(movie.get("id"))] = movie.get("title")
  return movies_map
