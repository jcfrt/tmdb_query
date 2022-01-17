from typing import Optional, Dict, Tuple
import requests
from json import dumps
from logging import getLogger
log = getLogger(__name__)

from . import API_KEY, API_BASE_URL, API_VERSION


class TMDB():
  BASE_PATH = ""
  # Dictionary of tuple pairs representing both path and HTTP method 
  # (GET, POST, DELETE, etc.) to be used to retrieve the info via 
  # the API: (info_type, method_type)
  SUB_PATH: Dict[str, Tuple[str, str]] = {}

  def __init__(self) -> None:
      self.base_url = API_BASE_URL
      self.base_url = f"{self.base_url}/{API_VERSION}"

  def _get_sub_path(self, key) -> str:
    return self.BASE_PATH + self.SUB_PATH[key][0]
  
  def _set_val_as_attrs(self, response) -> None:
    """Assign response values as object attributes."""
    if isinstance(response, dict):
      for key in response.keys():
        # Avoid overwriting methods, but allow overwriting any other attr
        if hasattr(self, key) and callable(getattr(self, key)):
          continue
        setattr(self, key, response[key])

  def _get(self, info_type, **kwargs) -> Dict:
    """
    Generic method to fetch a type of info, with optional payload depending
    on the method type.
    
    Args:
      info_type: str.
      payload: dict. Optional data for POST, DELETE http methods.
      kwargs: dict. Any valid keyword argument for a given query.
    Returns:
      A response as a JSON dict.
    """
    if info_type not in self.SUB_PATH.keys():
      raise Exception("Not a valid info type.")

    path = self._get_sub_path(info_type)
    # Replace placeholders with attribute value of the same key name.
    attr_map = {}
    for key in self.__dict__.keys():
      if not callable(getattr(self, key)):
        attr_map[key] = getattr(self, key)
    path = path.format_map(attr_map)

    method = self.SUB_PATH[info_type][1]
    
    # Some methods may require a request body:
    payload = kwargs.pop("payload", None)
    res = self._call_api(path, method, params=kwargs, data=payload)
    self._set_val_as_attrs(res)
    return res

  def _call_api(
    self,
    endpoint, 
    method: str, 
    params={}, 
    data: Optional[Dict] = None) -> Dict:
    """
    Args:
      method: str. Get, Post, Delete...
      params: dict. Key-value parameters for the URL
      data: dict <optional>. Payload to send with POST or DELETE HTTP methods.
    Returns:
      A response as a JSON dict.
    """
    full_url = f"{self.base_url}/{endpoint}"
    # For v4:
    # headers = {"Authorization": f"Bearer {API_TOKEN}", "Content-Type": "application/json;charset=utf-8"}
    params.update({ "api_key": API_KEY })

    response = getattr(requests, method.lower())(
      full_url, 
      params=params, 
      data=dumps(data) if data else data
    )

    log.debug(f"Fetched URL: {response.url}")

    response.raise_for_status()
    return response.json()
