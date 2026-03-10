#Simple API wrapper for TMDB 
import requests

BASE_URL = "https://api.themoviedb.org/3"
API_KEY = "8b3549b6ca7e044a906dea4d61a34125"


#Takes user query and returns search results.
def search_movies(query):
    url = BASE_URL + "/search/movie"
    response = requests.get(url, params={"api_key": API_KEY, "query":query})
    return response.json().get("results", [])
    
#Takes movie ID and returns movie details.    
def get_movie(movie_id):
    url = BASE_URL + "/movie/" + str(movie_id)
    response = requests.get(url, params={"api_key": API_KEY})
    return response.json().get("results", [])


