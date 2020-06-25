from django.urls import path
from .views import ProfileUpdateView, TelegramOTPView, ProfileFollowingView, ProfileDiscussionView, ProfileCommentView, ProfileReviewView
from allauth.account.views import PasswordChangeView
# from .views import SocialLoginView

urlpatterns = [
    path('update/', ProfileUpdateView.as_view(), name='update_profile'),
    path('telegram_otp/', TelegramOTPView.as_view(), name='telegram_otp'),
    path('password/', PasswordChangeView.as_view(), name='change_password'),
    path('profile/<slug:username>/following/', ProfileFollowingView.as_view(), name='profile_following'),
    path('profile/<slug:username>/comment/', ProfileCommentView.as_view(), name='profile_comment'),
    path('profile/<slug:username>/discussion/', ProfileDiscussionView.as_view(), name='profile_discussion'),
    path('profile/<slug:username>/review/', ProfileReviewView.as_view(), name='profile_review'),


    # path('google/login/', SocialLoginView.as_view(), name='google_login'),
]
