import unittest
from unittest import mock
from cli import *
from tmdb_client.exceptions import NotAnActor, NameNotFound

# Run with python -m pytest -vv -s --maxfail=10


class TestActorSearch(unittest.TestCase):
  valid_actors = { "Keanu Reeves", "Laurence Fishburne" }
  # Note that these examples may fail in the future as new actors crop up!
  invalid_actors = { "Jean-Pierre Jeunet" }
  unknown_persons = { "Lawrence Fishburne" }
  homonymous_actors = { "Michelle Williams" }

  def test_search_actor_by_name(self):
    for name in self.valid_actors:
      assert search_actor_by_name(name).get("id") is not None

    for name in self.invalid_actors:
      with self.assertRaises(NotAnActor):
        search_actor_by_name(name)

    for name in self.unknown_persons:
      with self.assertRaises(NameNotFound):
        search_actor_by_name(name)

  @mock.patch('cli.input')
  def test_homonymous_actors(self, mock_input):
    # Simulate selecting the first result
    mock_input.return_value = "1"

    for name in self.homonymous_actors:
      assert search_actor_by_name(name).get("id") is not None


class TestQuery(unittest.TestCase):
  persons = {"Keanu Reeves", "Laurence Fishburne"}
  expected = [
    "The Matrix",
    "Making 'The Matrix'",
    "The Matrix Revisited",
    "The Matrix Reloaded",
    "MTV Reloaded",
    "The Matrix Reloaded: Pre-Load",
    "The Matrix Revolutions",
    "The Matrix Revolutions Revisited",
    "The Matrix Reloaded Revisited",
    "A Man's Story",
    "John Wick: Chapter 2",
    "John Wick: Chapter 3 - Parabellum",
    "John Wick: Chapter 4"
  ]

  def test_discover_movies_for_ids(self):
    """Use the convenience methor provided by the API."""
    actor_ids = set()
    for name in self.persons:
      actor_ids.add(get_ensured_actor_id(name))
    assert len(actor_ids) == len(self.persons)
    movie_titles = discover_movies_for_ids(actor_ids)
    assert len(movie_titles) > 0
    for expected_title in self.expected:
      assert expected_title in movie_titles
    print(f"Found movies: {movie_titles}. Expected: {self.expected}")


  def test_get_common_movies_for_ids(self):
    """Use the slower method by looking up in each cast of each movie."""
    actor_ids = set()
    for name in self.persons:
      actor_ids.add(get_ensured_actor_id(name))
    assert len(actor_ids) == len(self.persons)
    movie_titles = get_common_movies_for_ids(actor_ids)
    assert len(movie_titles) > 0
    for expected_title in self.expected:
      assert expected_title in movie_titles
    print(f"Found movies: {movie_titles}. Expected: {self.expected}")
