import django
django.setup()

# export DJANGO_SETTINGS_MODULE=Empire_of_Movies.settings

import os

os.environ['DJANGO_SETTINGS_MODULE'] = 'Empire_of_Movies.settings'

from articles.models import Movie
movie_list = Movie.objects.all()
for movie in movie_list:
    movie.update()