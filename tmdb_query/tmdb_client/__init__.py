from os import environ

API_KEY = environ.get("TMDB_API_KEY", "")
API_BASE_URL = "https://api.themoviedb.org"
API_VERSION = 3

if len(API_KEY) != 32:
  raise Exception(
    "Invalid API key length. Should be 128 bits hexadecimal value. "
    f"Length was {len(API_KEY)}.")
try:
  int(API_KEY, 16)
except:
  raise Exception("Invalid API key. Must be 128 bits hexadecimal value.")