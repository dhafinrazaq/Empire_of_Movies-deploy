from django.db import models
from django.urls import reverse, reverse_lazy
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth import get_user_model
from notifications.models import Notification
from api import get_imdb_json

class Movie(models.Model):
    author = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        null=True, blank=True
    )
    year = models.CharField(max_length=255, null=True, blank=True)
    title = models.CharField(max_length=255, null=True, blank=True)
    synopsis = models.TextField(null=True, blank=True)
    image = models.TextField(null=True, blank=True)
    releaseDate = models.CharField(max_length=255, null=True, blank=True)
    runtimeStr = models.CharField(max_length=255, null=True, blank=True)
    directors = models.TextField(null=True, blank=True)
    writers = models.TextField(null=True, blank=True)
    stars = models.TextField(null=True, blank=True)
    genres = models.TextField(null=True, blank=True)
    companies = models.TextField(null=True, blank=True)
    countries = models.TextField(null=True, blank=True)
    languages = models.TextField(null=True, blank=True)
    contentRating = models.CharField(max_length=255, null=True, blank=True)
    imDbRating = models.CharField(max_length=255, null=True, blank=True)
    tagline = models.CharField(max_length=255, null=True, blank=True)
    keywords = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self): 
        return self.title

    def get_absolute_url(self):
        return reverse('movie_detail', args=[str(self.id)])

    def all_followers(self):
        return self.follower.all()

    @classmethod
    def create(self, id):
        json = get_imdb_json(id)
        if(json != None):
            movie = self(year=json.get('year'), title=json.get('title'), image=json.get('image'), synopsis=json.get('plot'), \
            releaseDate=json.get('releaseDate'), runtimeStr=json.get('runtimeStr'), directors=json.get('directors'), \
                writers=json.get('writers'), stars=json.get('stars'), genres=json.get('genres'), \
                    companies=json.get('companies'), countries=json.get('countries'), languages=json.get('languages'), \
                        imDbRating=json.get('imDbRating'), tagline=json.get('tagline'), keywords=json.get('keywords'))
            return movie
        else:
            return None

class Discussion(models.Model):
    title = models.CharField(max_length=255)
    body = models.TextField()
    author = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
    )
    date = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    movie = models.ForeignKey(
        Movie,
        on_delete=models.CASCADE,
        related_name='discussion',
        blank=True,
        null=True,
    )
    
    @classmethod
    def create(self, movie, title, body, author):
        discussion = self(title=title, author=author, body=body, movie=movie)
        return discussion

    def __str__(self): 
        return self.title or ' '

    def get_absolute_url(self):
        return reverse('discussion_detail', args=[str(self.movie.id), str(self.id)])

class Review(models.Model):
    author = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        null = True,
        blank = True,
    )
    title = models.CharField(max_length=255, null=True, blank=True)
    rating = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(10)])
    body = models.TextField()
    date = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    movie = models.ForeignKey(
        Movie,
        on_delete=models.CASCADE,
        related_name='review',
        
    )
    author = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        null=True, 
        blank=True
    )

    @classmethod
    def create(self, movie, title, body, rating, author):
        review = self(title=title, author=author, body=body, rating=rating, movie=movie)
        return review

    def __str__(self): 
        return self.title or ' '

    def get_absolute_url(self):
        return reverse('review_detail', args=[str(self.movie.id), str(self.id)])

class Comment(models.Model):
    title = models.TextField()
    author = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    date = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    discussion = models.ForeignKey(
        Discussion,
        on_delete=models.CASCADE,
        related_name='comment',
        null=True,
        blank=True,
    )
    
    def __str__(self): 
        return self.title or ' '

    def get_absolute_url(self):
        return reverse('comment_detail', args=[str(self.discussion.movie.pk), str(self.discussion.pk), str(self.pk)])
        # return reverse('home')

    @classmethod
    def create(self, title, author, discussion):
        comment = self(title=title, author=author, discussion=discussion)
        return comment