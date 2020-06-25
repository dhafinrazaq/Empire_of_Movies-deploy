from django.urls import path
from .views import ProfileUpdateView, TelegramOTPView, ProfileView
from allauth.account.views import PasswordChangeView
# from .views import SocialLoginView

urlpatterns = [
    path('update/', ProfileUpdateView.as_view(), name='update_profile'),
    path('telegram_otp/', TelegramOTPView.as_view(), name='telegram_otp'),
    path('password/', PasswordChangeView.as_view(), name='change_password'),
    path('profile/<slug:username>/', ProfileView.as_view(), name='profile_view'),


    # path('google/login/', SocialLoginView.as_view(), name='google_login'),
]
