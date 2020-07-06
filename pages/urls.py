from django.urls import path
from .views import HomePageDiscussion, PrivacyPolicyView, HomePageReview, HomePageLoginDiscussion, HomePageLoginReview

urlpatterns = [
path('', HomePageDiscussion.as_view(), name='home'),
path('review/', HomePageReview.as_view(), name='home_review'),
path('discussion_followed/', HomePageLoginDiscussion.as_view(), name='home_login_discussion'),
path('review_followed/', HomePageLoginReview.as_view(), name='home_login_review'),
path('privacy_policy/', PrivacyPolicyView.as_view(), name='privacy_policy'),
]