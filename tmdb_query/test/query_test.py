import sys
import unittest
import pytest
from ..tmdb_client.tmdb import TMDB
from tmdb_query.__main__ import print_common_movies, search_actor_by_name

# Run with pytest -vv -s --maxfail=10 test/unit_tests.py

persons = ["Keanu Reeves", "Lawrence Fishburne", "Carrie-Anne Moss"]
expected = """The Matrix
The Matrix Reloaded Revisited
Making 'The Matrix'
The Matrix Revisited
The Matrix Recalibrated
The Matrix Reloaded: Pre-Load
The Matrix Revolutions Revisited
The Matrix Resurrections
The Matrix Reloaded
The Matrix Revolutions
The Matrix Reloaded: Car Chase
"""

@pytest.mark.parametrize(
  ("test_input", "expected"),
  [
    (persons, expected)
  ]
)
def test_print_common_movies(test_input, expected):
  assert print_common_movies(test_input) == expected


def test_search_actor_by_name():
  for name in persons:
    assert search_actor_by_name(name).get("results") is not None
