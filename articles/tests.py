
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from django.test import Client, TestCase
from django.urls import reverse

from .models import Movie, Discussion, Review, Comment


class MovieTests(TestCase):

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

    def test_movie_listing(self):
        self.assertEqual(f'{self.movie.title}', 'Harry Potter')
        self.assertEqual(f'{self.movie.synopsis}', 'Once upon a time')
        self.assertEqual(f'{self.movie.year}', '2002')

    def test_movie_list_view_for_logged_in_user(self):
        self.client.login(username='user', password='testpass123')
        response = self.client.get(reverse('movie_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Harry Potter')
        self.assertTemplateUsed(response, 'movies/movie_list.html')

    def test_movie_list_view_for_logged_out_user(self):
        self.client.logout()
        response = self.client.get(reverse('movie_list'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '%s?next=/movies/list/' % (reverse('account_login')))
        response = self.client.get('%s?next=/movies/list/' % (reverse("account_login")))
        self.assertContains(response, 'Log In')

    def test_movie_detail_view_with_permissions(self):
        self.client.login(username='user', password='testpass123')
        response = self.client.get(self.movie.get_absolute_url())
        no_response = self.client.get('/movies/12345/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(no_response.status_code, 404)
        self.assertContains(response, 'Harry Potter')
        self.assertContains(response, 'Once upon a time')
        self.assertTemplateUsed(response, 'movies/movie_detail.html')

class ReviewTests(TestCase):

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
        self.review = Review.objects.create(
            title='Review title',
            body='Body of review',
            movie=self.movie,
            author=self.user,
            rating=7,
        )

    def test_review_list_view_for_logged_in_user(self):
        self.client.login(username='user', password='testpass123')
        response = self.client.get(reverse('review_list', args=[self.movie.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Review title')
        self.assertTemplateUsed(response, 'reviews/review_list.html')

    def test_review_list_view_for_logged_out_user(self):
        self.client.logout()
        response = self.client.get(reverse('review_list', args=[self.movie.pk]))
        self.assertEqual(response.status_code, 302)

    def test_review_detail_view(self):
        self.client.login(username='user', password='testpass123')
        response = self.client.get(self.review.get_absolute_url())
        no_response = self.client.get('movies/12345/review/123')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(no_response.status_code, 404)
        self.assertContains(response, 'Review title')
        self.assertContains(response, 'Body of review')
        self.assertTemplateUsed(response, 'reviews/review_detail.html')

class DiscussionTests(TestCase):

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
        self.discussion = Discussion.objects.create(
            title='Discussion title',
            body='Body of discussion',
            movie=self.movie,
            author=self.user,
        )

    def test_discussion_list_view_for_logged_in_user(self):
        self.client.login(username='user', password='testpass123')
        response = self.client.get(reverse('discussion_list', args=[self.movie.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Discussion title')
        self.assertTemplateUsed(response, 'discussions/discussion_list.html')

    def test_discussion_list_view_for_logged_out_user(self):
        self.client.logout()
        response = self.client.get(reverse('discussion_list', args=[self.movie.pk]))
        self.assertEqual(response.status_code, 302)

    def test_discussion_detail_view(self):
        self.client.login(username='user', password='testpass123')
        response = self.client.get(self.discussion.get_absolute_url())
        no_response = self.client.get('movies/12345/discussion/123')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(no_response.status_code, 404)
        self.assertContains(response, 'Discussion title')
        self.assertContains(response, 'Body of discussion')
        self.assertTemplateUsed(response, 'discussions/discussion_detail.html')

class CommentTests(TestCase):

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
        self.discussion = Discussion.objects.create(
            title='Discussion title',
            body='Body of discussion',
            movie=self.movie,
            author=self.user,
        )
        self.comment = Comment.objects.create(
            title='Comment title',
            discussion=self.discussion,
            author=self.user,
        )

    def test_comment_detail_view(self):
        self.client.login(username='user', password='testpass123')
        response = self.client.get(self.comment.get_absolute_url())
        no_response = self.client.get('movies/12345/discussion/123/comment/1234')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(no_response.status_code, 404)
        self.assertContains(response, 'Comment title')
        self.assertTemplateUsed(response, 'comment/comment_detail.html')