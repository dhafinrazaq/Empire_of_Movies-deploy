from .models import Movie

def add_variable_to_context(request):
    return {
        'movie_list_base': Movie.objects.all()
    }