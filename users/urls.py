from django.urls import path
from .views import ProfileUpdateView, TelegramOTPView
from allauth.account.views import PasswordChangeView
urlpatterns = [
    path('update/', ProfileUpdateView.as_view(), name='update_profile'),
    path('telegram_otp/', TelegramOTPView.as_view(), name='telegram_otp'),
    path('password/', PasswordChangeView.as_view(), name='change_password'),
]
