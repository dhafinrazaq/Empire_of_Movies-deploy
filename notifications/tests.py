from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from django.test import Client, TestCase
from django.urls import reverse

from .models import Notification
from articles.models import Movie, Discussion

from django.test import TestCase
from .models import Notification
# Create your tests here.
class NotificationsTests(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='user',
            email='user@email.com',
            password='testpass123'
        )
        self.movie = Movie.objects.create(
            title='Harry Potter',
            synopsis='Once upon a time',
            year='2002'
        )
        self.user.follows.add(self.movie)


    def test_notification_list_view_for_logged_in_user(self):
        self.client.login(username='user', password='testpass123')
        self.client.post(reverse('discussion_new', args=[self.movie.pk]), {'author':self.user, 'title': "Discussion title", 'body':"Discussion body", 'movie':self.movie})
        response = self.client.get(reverse('notification_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Discussion title')
        self.assertTemplateUsed(response, 'notifications/notification_list.html')
