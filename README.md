
This program queries the REST API of the TheMoviesDataBase for movies where actors have both played.

# Dependencies

```
python3.8
requests
```
Python dependencies can be installed with `pip install -r requirements.txt`

# Usage

A valid TMDB API key is required to be set as an environment variable.

```
> export TMDB_API_KEY="MY_KEY"
> python3 tmdb_query --help
Usage: tmdb_query "Actor Name 1" "Actor Name 2"
```

## Example:
```
> python3 tmdb_query.py "Keanu Reeves" "Laurence Fishburne"
Found 13 movies in which Keanu Reeves and Laurence Fishburne have played (sorted by release date):
The Matrix
Making 'The Matrix'
The Matrix Revisited
The Matrix Reloaded
MTV Reloaded
The Matrix Reloaded: Pre-Load
The Matrix Revolutions
The Matrix Revolutions Revisited
The Matrix Reloaded Revisited
A Man's Story
John Wick: Chapter 2
John Wick: Chapter 3 - Parabellum
John Wick: Chapter 4
```

## Running tests:

Using `pytest` is recommended. It should be run while the current working directory is ./tmdb_query.

# TODO

* Tests: Cache API response as fixtures to avoid testing over the wire, or use mocks.
* Package and setup.

# Acknowledgement

This program uses the TMDB API but is not endorsed or certified by TMDB. 
Some parts have been loosely inspired by the tmdbsimple library written by Celia Oakley.
