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
    response = requests.get(url, params={"api_key": API_KEY, "append_to_response": "credits"})
    return response.json()

#Takes movie object and prints movie details.
def print_movie_details(movie):
    print(movie["title"])  
    print(movie["release_date"])    
    for genre in movie["genres"]:
        print(genre["name"]) 

#Gets Genre IDs
def get_genres():
    url = BASE_URL + "/genre/movie/list"
    response = requests.get(url, params={"api_key": API_KEY})
    genres = response.json().get("genres", [])
    return genres

def search_movies_genre_filter(genre_id):
    url = BASE_URL + "/discover/movie"
    response = requests.get(url, params = {"api_key": API_KEY, "with_genres": genre_id})
    return response.json().get("results", [])
