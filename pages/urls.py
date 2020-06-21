from django.urls import path
from .views import HomePageView, PrivacyPolicyView

urlpatterns = [
path('', HomePageView.as_view(), name='home'),
path('privacy_policy/', PrivacyPolicyView.as_view(), name='privacy_policy'),
]