import requests
import json
import ast
from django.conf import settings

omdb_api_key = settings.OMDB_API_KEY
imdb_api_key = settings.IMDB_API_KEY

def get_imdb_rating(id):
        imdb_api_url = "https://imdb-api1.p.rapidapi.com/Title/{}/{}".format(imdb_api_key, str(id))
        headers = {
            'x-rapidapi-host': "imdb-api1.p.rapidapi.com",
            'x-rapidapi-key': "da78a6df11msh96f14ac6607fb8dp1dccccjsn9f75e52b9332"
        }

        imdb_api_response = requests.request("GET", imdb_api_url, headers=headers)

        imdb_api_json = imdb_api_response.json()
        rating = imdb_api_json.pop('imDbRating')
        return rating



def get_imdb_json(id):
    if (isinstance(id, str)):
        imdb_api_url = "https://imdb-api1.p.rapidapi.com/Title/{}/{}".format(imdb_api_key, str(id))
        headers = {
            'x-rapidapi-host': "imdb-api1.p.rapidapi.com",
            'x-rapidapi-key': "da78a6df11msh96f14ac6607fb8dp1dccccjsn9f75e52b9332"
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
    omdb_url = 'http://www.omdbapi.com/?apikey={}&t={}&y={}'.format(omdb_api_key, request_title, request_year) 
    

    omdb_response = requests.request("GET", omdb_url)
    omdb_json = omdb_response.json()
    id = omdb_json.get('imdbID')
    if (isinstance(id, str)):
        imdb_api_url = "https://imdb-api1.p.rapidapi.com/Title/{}/{}".format(imdb_api_key, str(id))
        headers = {
            'x-rapidapi-host': "imdb-api1.p.rapidapi.com",
            'x-rapidapi-key': "da78a6df11msh96f14ac6607fb8dp1dccccjsn9f75e52b9332"
        }

        imdb_api_response = requests.request("GET", imdb_api_url, headers=headers)

        imdb_api_json = imdb_api_response.json()
        similars = imdb_api_json.pop('similars')
        possible_movies = []
        possible_movies.append([imdb_api_json.get('id'), imdb_api_json.get('title'), imdb_api_json.get('year')])
        for similar in similars:
            possible_movies.append([similar.get('id'), similar.get('title'), similar.get('year')])
        # print(possible_movies)
        return possible_movies
    else:
        return None
