import requests
import json
import ast

def get_imdb_rating(id):
        imdb_api_url = "https://imdb-api1.p.rapidapi.com/Title/k_7z9iNr0H/" + id
        headers = {
            'x-rapidapi-host': "imdb-api1.p.rapidapi.com",
            'x-rapidapi-key': "2f744174a8msh81a79fd4c738d7dp1b81e4jsn0ce24b827fa5"
            }

        imdb_api_response = requests.request("GET", imdb_api_url, headers=headers)

        imdb_api_json = imdb_api_response.json()
        rating = imdb_api_json.pop('imDbRating')
        return rating



def get_imdb_json(id):
    if (isinstance(id, str)):
        imdb_api_url = "https://imdb-api1.p.rapidapi.com/Title/k_7z9iNr0H/" + id
        headers = {
            'x-rapidapi-host': "imdb-api1.p.rapidapi.com",
            'x-rapidapi-key': "2f744174a8msh81a79fd4c738d7dp1b81e4jsn0ce24b827fa5"
            }

        imdb_api_response = requests.request("GET", imdb_api_url, headers=headers)

        imdb_api_json = imdb_api_response.json()
        similars = imdb_api_json.pop('similars')

        return imdb_api_json
    else:
        return None

def get_possible_movies(title, year):
    request_title = title
    request_year = year
    omdb_url = 'http://www.omdbapi.com/?apikey=fb722e07&t=' + request_title + '&y=' + request_year
    

    omdb_response = requests.request("GET", omdb_url)
    omdb_json = omdb_response.json()
    id = omdb_json.get('imdbID')
    if (isinstance(id, str)):
        imdb_api_url = "https://imdb-api1.p.rapidapi.com/Title/k_7z9iNr0H/" + id
        headers = {
            'x-rapidapi-host': "imdb-api1.p.rapidapi.com",
            'x-rapidapi-key': "2f744174a8msh81a79fd4c738d7dp1b81e4jsn0ce24b827fa5"
            }

        imdb_api_response = requests.request("GET", imdb_api_url, headers=headers)

        imdb_api_json = imdb_api_response.json()
        similars = imdb_api_json.pop('similars')
        possible_movies = []
        possible_movies.append([imdb_api_json.get('id'), imdb_api_json.get('title'), imdb_api_json.get('year')])
        for similar in similars:
            possible_movies.append([similar.get('id'), similar.get('title'), similar.get('year')])
        print(possible_movies)
        return possible_movies
    else:
        return None