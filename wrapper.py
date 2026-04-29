#Simple API wrapper for TMDB 
import requests
import threading
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


def get_final_recommendation(favorite_ids=None):
    seen_ids = set()
    frequency = {}
    popularity = {}
    final = []
    results = {}

    if favorite_ids:
        seen_ids.update(favorite_ids)

    # Fetch all recommendations at the same time using threads
    def fetch(movie_id):
        results[movie_id] = get_recommendations(movie_id)

    threads = []
    for movie_id in (favorite_ids or []):
        t = threading.Thread(target=fetch, args=(movie_id,))
        threads.append(t)
        t.start()

    # Wait for all threads to finish
    for t in threads:
        t.join()

    # Process results
    for movie_id in (favorite_ids or []):
        for movie in results.get(movie_id, []):
            if movie["id"] not in seen_ids:
                seen_ids.add(movie["id"])
                frequency[movie["id"]] = frequency.get(movie["id"], 0) + 1
                popularity[movie["id"]] = movie.get("popularity", 0)
                final.append(movie)
            else:
                frequency[movie["id"]] = frequency.get(movie["id"], 0) + 1

    final = [m for m in final if m.get("vote_average", 0) >= 6.0]
    final.sort(key=lambda m: (frequency.get(m["id"], 0), popularity.get(m["id"], 0)), reverse=True)
    return final[:10]