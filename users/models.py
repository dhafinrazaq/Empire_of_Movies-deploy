from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.postgres.fields import ArrayField
import hashlib
from django.urls import reverse

# Create your models here.
class CustomUser(AbstractUser):
    telegram_id = models.CharField(max_length=255, null=True, blank=True)
    chat_id = models.CharField(max_length=255, null=True, blank=True)
    follows = models.ManyToManyField('articles.Movie', related_name='follower', blank=True)
    upvotes_discussion = models.ManyToManyField('articles.Discussion', related_name='discussion_upvoter', blank=True)
    downvotes_discussion = models.ManyToManyField('articles.Discussion', related_name='discussion_downvoter', blank=True)
    notifications = models.ManyToManyField('notifications.Notification', related_name='notified', blank=True)
    OTP = models.IntegerField(null=True, blank=True)
    receive_email = models.BooleanField(default=True)
    
    
    def hash(self):
        return int(hashlib.sha256(self.username.encode('utf-8')).hexdigest(), 16) % 10**8

    def have_notification(self):
        return self.notifications.all().count() > 0

    def all_notification(self):
        return self.notifications.all()

    def get_absolute_url(self):
        return reverse('profile_following', args=[str(self.username)])
