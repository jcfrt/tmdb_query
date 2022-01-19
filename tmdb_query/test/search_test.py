import unittest
from typing import List, Any
import tmdb_client.search
from test.movie_test import TV_NAME, MOVIE_ID, MOVIE_NAME
from test.person_test import PERSON_ID, PERSON_NAME


def iterate_results(results: List, look_for: Any, key: str) -> bool:
  """
  Look for "look_for" value at key for each item in results.
  """
  found = False
  for movie_entry in results:
    if movie_entry.get(key) == look_for:
      found = True
      break
  return found


class SearchTestCase(unittest.TestCase):
  def test_search_movie(self):
    search = tmdb_client.search.Search()
    search.movie(query=MOVIE_NAME)
    assert hasattr(search, "results")
    results = getattr(search, "results")
    assert iterate_results(results, MOVIE_ID, "id")

  def test_search_person(self):
    search = tmdb_client.search.Search()
    search.person(query=PERSON_NAME)
    assert hasattr(search, "results")
    results = getattr(search, "results")
    assert iterate_results(results, PERSON_ID, "id")


class DiscoverTestCase(unittest.TestCase):
  def test_discover_movie(self):
    discover = tmdb_client.search.Discover()
    discover.movie(query=MOVIE_NAME)
    assert hasattr(discover, "results")

  def test_discover_tv(self):
    discover = tmdb_client.search.Discover()
    discover.tv(query=TV_NAME)
    assert hasattr(discover, "results")
