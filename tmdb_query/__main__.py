import sys
import logging
from typing import AbstractSet, List, Dict
from .tmdb_client.person import Person
from .tmdb_client.movie import Movie
from .tmdb_client.search import Discover, Search
from .tmdb_client.util import add_all_to, any_title
from .tmdb_client.exceptions import *

log = logging.getLogger("tmdb_client")
logging.basicConfig()
# log.setLevel(logging.DEBUG)

args = sys.argv[1:]

args = [a.strip("\" \'") for a in args]
# Make sure we don't have duplicates
args = set(args)

if len(args) < 2 or "--help" in args:
  print(f"Usage: {sys.argv[0]} \"Actor Name 1\" \"Actor Name 2\" ...")
  exit(0)


def search_actor_by_name(name: str) -> Dict:
  """
  For a given name, get the dictionary-like object returned by the Search API
  enpoint of TMDB, filtering out people who are not known for being actors.
  This may require user input if homonyms are found.
  Args:
    name: str. Name of the actor to lookup.
  Returns:
    A dictionary representing a Search result for this actor.
  """
  lookup = Search()
  log.debug(f"Lookup for \"{name}\":\n{lookup.person(query=name)}")

  results = getattr(lookup, "results", [])
  if not results:
    raise NameNotFound(f"No result found for name \"{name}\".")

  # We only care about actors
  results = [n for n in results if n.get("known_for_department", "") == "Acting"]  
  if not results:
    raise NotAnActor(f"No actor found named \"{name}\".")

  if len(results) == 1:
    print(
      "Found one actor named \"{}\", known for: {}.".format(
        name,
        ", ".join(any_title(n) for n in results[0].get("known_for", []))
      )
    )
  # Handling homonymous people requires user input
  else:
    print(f"Found more than one actor with the name \"{name}\"."
          "Please select an actor:")
    for result in results:
      print(
        "{}. {}, known for: {}.".format(
          results.index(result), 
          name,
          ", ".join(any_title(n) for n in result.get("known_for", [])))
      )

    input_index = -1
    while input_index < 0 or input_index > len(results):
      input_index = int(input("Input a choice number: "))
    return results[input_index]

  return results[0]


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


def get_common_movies_for_ids(actor_ids: AbstractSet[int]) -> List[str]:
  """
  Retrieve movies where all actors in actors_ids were part of the cast.
  This method is particularly slow. It retrieves all movies where an actor was 
  part of the cast, and for each movie it checks if the other actor ids are also
  part of the cast. This can potentially make a lot of API requests.
  Args:
    actor_ids: set. Set of actor ids as ints.
  Returns:
    A list of movie titles as strings.
  """
  common_movies_map: Dict[int, str] = {}
  for actor_id in actor_ids:
    other_actors = [a_id for a_id in actor_ids if a_id is not actor_id]
    # Get all movies 
    movie_ids = get_movies_id_for_actor_id(actor_id)
    log.debug(f"movie_ids {movie_ids}")
    for movie_id, movie_title in movie_ids.items():
      for cast_id in get_movie_cast(movie_id):
        if cast_id in other_actors:
          common_movies_map[movie_id] = movie_title
    if len(actor_ids) <= 2:
      # No need to check the other actor if we only have 2.
      break
  return [m for m in common_movies_map.values()]


def discover_movies_for_ids(actor_ids: AbstractSet[int]) -> List[str]:
  """
  Use the Discover TMDB API method to get movies where all actors in actors_ids 
  were part of the cast.
  This is the preferred way of retrieving such information since the TMDB does
  all the work for us. Results are sorted by release date.
  Args:
    actor_ids: set. Set of actor ids as ints.
  Returns:
    A list of movie titles as strings.
  """
  # The TMDB API already provides us with a convenience method to get movies
  # with this cast combination:
  d = Discover()
  params = {
    "with_cast": ",".join((str(_id) for _id in actor_ids)),
    "sort_by": "release_date.asc"
  }
  # This should translate to an enpoint similar to:
  # f"discover/movie?with_cast=Name1,Name2&sort_by=release_date.asc"
  _json = d.movie(**params)
  total_results = _json.get("total_results", 0)
  movies = []
  if not total_results:
    return movies

  add_all_to(movies, d)
  # Fetch all remaining pages:
  while getattr(d, "page") < getattr(d, "total_pages", 1):
    params.update( {"page": str(getattr(d, "page") + 1)} )
    _json = d.movie(**params)
    add_all_to(movies, d)

  return movies


def print_common_movies(names: AbstractSet[str]) -> None:
  """
  Find movies for which all actors in names have been cast together and
  prints them to stdout.
  Args:
    names: set of strings. Names of the actors to look up.
  Returns:
    None
  """
  actor_ids = set()

  for name in names:
    name = name.strip()
    search_result = search_actor_by_name(name)
    if not is_actor(search_result):
      raise NotAnActor(f"\"{name}\" is not known for being an actor.")
    else:
      log.debug(f"{name} seems to be an actor.")
    
    if actor_id := search_result.get("id"):
      actor_ids.add(int(actor_id))
    else:
      raise Exception(f"No id found for name {name}.")

  log.debug(f"Actor ids: {actor_ids}")
  if len(actor_ids) < 2:
    raise Exception("Not enough valid actors found from these names.")

  # Fast method provided by the TMDB API: 
  movies = discover_movies_for_ids(actor_ids)
  
  # Much slower method:
  # movies = get_common_movies_for_ids(actor_ids)

  if not len(movies):
    print("No movie found where these two actors were cast together.")
    return

  print(
    f"Found {len(movies)} movies in which {' and '.join(args)} have played "
    "(sorted by release date):")
  for title in movies:
    print(title)


print_common_movies(args)
