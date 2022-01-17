from typing import List, Dict, Any


def add_all_to(str_list: List, obj: object):
  """Add each element in the .results attribute from obj to the list pointed
  at by str_list.
  Args:
    str_list: list. The list to append to.
    obj: object. The object from which to read the "results" attribute.
  """
  for el in getattr(obj, "results", []):
    str_list.append(el.get("title"))


MEDIA_TITLE_KEYS = [
  "original_name", "name", "original_title"
]

def any_title(entry: Dict) -> Any:
  """Retrieve the first key found from entry."""
  for key in MEDIA_TITLE_KEYS:
    if value := entry.get(key):
      return value