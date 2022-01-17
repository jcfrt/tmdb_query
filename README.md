
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
> python3 tmdb_query.py "Keanu Reeves" "Lawrence Fishburne" "Carrie-Anne Moss"
Found 11 movies in which Carrie-Anne Moss and Keanu Reeves and Laurence Fishburne have played (sorted by release date):
The Matrix
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
```

# Acknowledgement

This program uses the TMDB API but is not endorsed or certified by TMDB. 
Some parts have been loosely inspired by the tmdbsimple library written by Celia Oakley.