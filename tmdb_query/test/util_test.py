from tmdb_client.util import *
from test.movie_test import MOVIE_ID
from test.person_test import PERSON_ID

def test_add_all_to():
  class Object(object):
    pass
  obj = Object()
  setattr(obj, "results", [{"title": "a_title"}, {"title": "another_title"}])
  _list = []
  add_all_to(_list, obj)
  assert "a_title" in _list
  assert "another_title" in _list 


def test_get_first_known_key():
  _dict = {"a_title": "foo", "name": "bar", "a_key": "a_value"}
  assert get_first_known_key(_dict, ("name",)) == "bar"


def test_is_actor():
  a_valid_person = {"id": 1} # George Lucas
  not_an_actor = {"known_for_department": "Production"}
  an_actor = {"known_for_department": "Acting"}
  invalid = dict()
  assert is_actor(a_valid_person) == False
  assert is_actor(not_an_actor) == False
  assert is_actor(an_actor) == True
  raised = False
  try:
    is_actor(invalid)
  except:
    raised = True
  assert raised == True


def test_get_movie_cast():
  movie_id = MOVIE_ID
  assert len(get_movie_cast(movie_id)) > 0


def test_get_movies_id_for_actor_id():
  actor_id = PERSON_ID
  assert len(get_movies_id_for_actor_id(actor_id)) > 0


