#!/usr/bin/env python
import logging
import sys
import argparse
from typing import AbstractSet, List, Dict
from tmdb_client.search import Discover, Search
from tmdb_client.util import (
  add_all_to, get_first_known_key, get_movie_cast, 
  get_movies_id_for_actor_id, is_actor
)
from tmdb_client.exceptions import NotAnActor, NameNotFound

log = logging.getLogger("tmdb_client")
logging.basicConfig()
# log.setLevel(logging.DEBUG)


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
        ", ".join(get_first_known_key(n) for n in results[0].get("known_for", []))
      )
    )
  # Handling homonymous people requires user input
  else:
    print(f"Found more than one actor with the name \"{name}\"."
          "Please select an actor:")
    for result in results:
      print(
        "{}. {}, known for: {}.".format(
          results.index(result) + 1, 
          name,
          ", ".join(get_first_known_key(n) for n in result.get("known_for", [])))
      )

    input_index = -1
    while input_index < 1 or input_index > len(results):
      input_index = int(input("Input a choice number: "))
    return results[input_index - 1]

  return results[0]


def get_common_movies_for_ids(actor_ids: AbstractSet[int]) -> List[str]:
  """
  Retrieve movies where all actors in actor_ids were part of the cast.
  This method is particularly slow. It first retrieves all movies where an actor 
  was part of the cast, and for each movie it then checks if the other actor ids 
  are also part of the cast. Beware: this may potentially make a lot of API requests.
  Args:
    actor_ids: set. Set of actor ids as ints.
  Returns:
    A list of movie titles as strings.
  """
  common_movies_map: Dict[int, str] = {}
  
  for actor_id in actor_ids:
    other_actors = set([a_id for a_id in actor_ids if a_id is not actor_id])
    
    # Get all movies 
    movie_ids = get_movies_id_for_actor_id(actor_id)
    log.debug(f"Movie IDs: {movie_ids}")
    
    for movie_id, movie_title in movie_ids.items():
      cast_ids = get_movie_cast(movie_id)
      # Test if other_actors is a subset of cast_ids, which ensure that ALL the
      # other_actors are part of this movie's cast.
      if other_actors <= cast_ids:
        common_movies_map[movie_id] = movie_title
    
    if len(actor_ids) <= 2:
      # No need to check the other actor if we only have 2.
      log.debug("Only two actors compared. Ending movie cast lookup.")
      break
  log.debug(f"Found {len(common_movies_map)} movies: {common_movies_map}")
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


def get_common_movies(names: AbstractSet[str]) -> List[str]:
  """
  Find movies for which all actors in names have been cast together.
  Args:
    names: set of strings. Names of the actors to look up.
  Returns:
    A list of movie titles as strings.
  """
  actor_ids = set()
  for name in names:
    actor_id = get_ensured_actor_id(name)
    if actor_id < 0:
      raise NameNotFound(f"No id found for name {name}.")
    actor_ids.add(actor_id)

  log.debug(f"Actor ids: {actor_ids}")
  if len(actor_ids) < 2:
    raise Exception("Not enough valid actor names found from the submitted names.")

  # Fast method provided by the TMDB API: 
  return discover_movies_for_ids(actor_ids)
  
  # Much slower method:
  # return get_common_movies_for_ids(actor_ids)


def get_ensured_actor_id(name: str) -> int:
  """
  Search person by name, but ensure that is an actor.
  Args:
    name: str. Name of the person to lookup.
  Returns:
    The ID of the person if it is indeed an actor, otherwise returns -1.
  """
  name = name.strip()
  search_result = search_actor_by_name(name)
  if not is_actor(search_result):
    raise NotAnActor(f"\"{name}\" is not known for being an actor.")
  else:
    log.debug(f"{name} seems to be an actor.")
  
  if actor_id := search_result.get("id"):
    return int(actor_id)
  return -1


def main(args=None) -> int:
  parser = argparse.ArgumentParser(description='Look up movies where actors have all been part of the cast.')
  parser.add_argument(
    'persons', metavar='ACTORS', type=str, nargs='+',
    action="extend",
    help='actors to look up')

  pargs = parser.parse_args(args)

  persons = pargs.persons
  persons = [a.strip("\" \'") for a in persons]
  # Ensure we don't have duplicates:
  persons = set(persons)

  if len(persons) < 2:
    print(f"Error: at least 2 names need to be passed as arguments.")
    return 1

  movies = get_common_movies(persons)

  if not len(movies):
    print("No movie found where these two actors were cast together.")
    return 0

  print(
    f"Found {len(movies)} movies in which {' and '.join(persons)} have played "
    "(sorted by release date):")
  for title in movies:
    print(title)
  return 0


if __name__ == "__main__":
  sys.exit(main())
