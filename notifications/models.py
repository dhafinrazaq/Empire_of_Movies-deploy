from django.db import models
from django.urls import reverse
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth import get_user_model

class Notification(models.Model):
    title = models.CharField(max_length=255)
    movie_link = models.TextField()
    movie_title = models.TextField(blank=True, null=True)
    inside_link = models.TextField()
    inside_title = models.TextField(blank=True, null=True)
    date = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    
    def __str__(self): 
        return self.title


    @classmethod
    def create(self, title, movie, inside):
        notification = self(title=title, movie_link=movie.get_absolute_url(), inside_link=inside.get_absolute_url(), \
            movie_title=movie.title, inside_title=inside.title)
        return notification
    # def get_absolute_url(self):
    #     return reverse('notification_detail', args=[str(self.id)])

    def all_notified(self):
        return self.notified.all()

    