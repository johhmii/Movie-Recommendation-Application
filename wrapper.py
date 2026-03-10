#Simple API wrapper for TMDB 

import requests

BASE_URL = "https://api.themoviedb.org/3"
API_KEY = "eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiI4YjM1NDliNmNhN2UwNDRhOTA2ZGVhNGQ2MWEzNDEyNSIsIm5iZiI6MTc3MTg5Nzk5My4zMzQsInN1YiI6IjY5OWQwNDg5MzdkMmU0MDYyMDgwZjkyOCIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.e2LDAgcOCcJAra3VjXl-B81nErpwImxXOGZm0eh_6JE"

def search_movies(query):
    response = requests.get(f"{BASE_URL}/search/movie", params={"api_key": API_KEY, "query":query})
    return response.json().get("results", [])
    
