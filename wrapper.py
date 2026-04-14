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

# Takes movie ID and returns recommended movies
def get_recommendations(movie_id):
    url = BASE_URL + "/movie/" + str(movie_id) + "/recommendations"
    response = requests.get(url, params = {"api_key": API_KEY})
    return response.json().get("results", [])

# Takes movie ID and returns similar movies
def get_similar(movie_id):
    url = BASE_URL + "/movie/" + str(movie_id) + "/similar"
    response = requests.get(url, params = {"api_key": API_KEY})
    return response.json().get("results", [])

# Produces final recommendation mix of similar and recommended movies
def get_final_recommendation(movie_id, favorite_ids=None):
    recommendations = get_recommendations(movie_id)
    similar = get_similar(movie_id)

    seen_ids = set()
    final = []

    if favorite_ids:
        seen_ids.update(favorite_ids)
 
    i = 0

    while i<max(len(recommendations), len(similar)) and len(final) <5:
        if i<len(recommendations):
            movie = recommendations[i]
            if movie["id"] not in seen_ids:
                seen_ids.add(movie["id"])
                final.append(movie)
        if i<len(similar):
            movie = similar[i]
            if movie["id"] not in seen_ids:
                seen_ids.add(movie["id"])
                final.append(movie)
        i += 1
    return final