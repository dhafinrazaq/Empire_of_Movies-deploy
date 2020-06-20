from django.test import Client, TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse, resolve 
from .views import ProfileUpdateView
from .forms import CustomUserCreationForm 

# Create your tests here.
class CustomUserTests(TestCase):
    def test_create_user(self):
        User = get_user_model()
        user = User.objects.create_user(
            username='test123',
            email='test123@email.com',
            password = 'testpass123', 
            )
        self.assertEqual(user.username,'test123')
        self.assertEqual(user.email, 'test123@email.com')
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)

    def test_create_superuser(self):
        User = get_user_model()
        user = User.objects.create_superuser(
            username='test123',
            email='test123@email.com',
            password = 'testpass123', 
            )
        self.assertEqual(user.username,'test123')
        self.assertEqual(user.email, 'test123@email.com')
        self.assertTrue(user.is_active)
        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_superuser)

class SignupTests(TestCase): 
    username = 'newuser'
    email = 'newuser@email.com'

    def setUp(self):
        url = reverse('account_signup')
        self.response = self.client.get(url)

    def test_signup_template(self):
        self.assertEqual(self.response.status_code, 200)
        self.assertTemplateUsed(self.response, 'account/signup.html')
        self.assertContains(self.response, 'Sign Up')
        self.assertNotContains(
            self.response, 'Hi there! I should not be on the page.')

    def test_signup_form(self):
        new_user = get_user_model().objects.create_user(
            self.username, self.email)
        self.assertEqual(get_user_model().objects.all().count(), 1)
        self.assertEqual(get_user_model().objects.all()
                         [0].username, self.username)
        self.assertEqual(get_user_model().objects.all()
                         [0].email, self.email)

class UpdateProfileTest(TestCase): 

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='testuser',
            email='testuser@email.com',
            password='testpass123'
        )
        self.client.login(username='testuser', password='testpass123')
        self.response = self.client.get(reverse('update_profile'))

    def test_update_profile_template(self):
        self.assertEqual(self.response.status_code, 200)
        self.assertTemplateUsed(self.response, 'account/profile_update.html')
        self.assertContains(self.response, 'Update Profile')
        self.assertNotContains(
            self.response, 'Hi there! I should not be on the page.')