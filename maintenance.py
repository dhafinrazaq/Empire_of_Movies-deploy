
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Empire_of_Movies.settings')

import django
django.setup()


from articles.models import Movie
movie_list = Movie.objects.all()
for movie in movie_list:
    movie.update()