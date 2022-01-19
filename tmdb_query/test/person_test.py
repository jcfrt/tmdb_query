import unittest
import tmdb_client.person

PERSON_NAME = "Keanu Reeves"
PERSON_ID = 6384


class PersonTestCase(unittest.TestCase):
  def test_person_details(self):
    person = tmdb_client.person.Person(PERSON_ID)
    person.details()
    assert person.name == PERSON_NAME
  
  def test_person_combined_credits(self):
    person = tmdb_client.person.Person(PERSON_ID)
    person.combined_credits()
    assert hasattr(person, "cast")

  def test_movie_credits(self):
    person = tmdb_client.person.Person(PERSON_ID)
    person.combined_credits()
    assert hasattr(person, "cast")