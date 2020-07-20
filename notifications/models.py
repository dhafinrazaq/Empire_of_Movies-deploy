from django.db import models
from django.urls import reverse
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.conf import settings

class Notification(models.Model):
    title = models.CharField(max_length=255)
    movie_link = models.TextField(blank=True, null=True)
    movie_title = models.TextField(blank=True, null=True)
    inside_link = models.TextField(blank=True, null=True)
    inside_title = models.TextField(blank=True, null=True)
    date = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    
    def __str__(self): 
        return self.title

    @classmethod
    def create(self, title, movie, inside):
        notification = self(title=title, movie_link=movie.get_absolute_url(), inside_link=inside.get_absolute_url(), \
            movie_title=movie.title, inside_title=inside.title)
        
        subject = title + " " + movie.title + " with title " + inside.title
        message = title + " " + movie.title + " with title " + inside.title + ". To open it, click on the following link: https://empire-of-movies.herokuapp.com" + inside.get_absolute_url()
        email_from = settings.EMAIL_HOST_USER
        recipient_list = []    
        

        for follower in movie.follower.all():
            if (follower.receive_email):
                if (follower.email):
                    recipient_list.append(follower.email)

        send_mail(subject, message, email_from, recipient_list)

        return notification
    
    @classmethod
    def create_title(self, title):
        notification = self(title=title, movie_link=None, inside_link=None, \
            movie_title=None, inside_title=None)
        return notification

    def all_notified(self):
        return self.notified.all()

    