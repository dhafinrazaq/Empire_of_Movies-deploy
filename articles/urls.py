from django.urls import path
from .views import MovieFollowedTitleView, MovieFollowedLatestView, MovieListLatestView,MovieListTitleView, MovieDetailView, MovieEditView, MovieDeleteView, MovieCreateView, MovieListView, MovieFollowedView, MovieRequestView, MovieRequestListView
from .views import DiscussionDetailView, DiscussionEditView, DiscussionDeleteView, DiscussionCreateView, DiscussionListViewNew, DiscussionListViewTop
from .views import ReviewDetailView, ReviewEditView, ReviewDeleteView, ReviewCreateView, ReviewListView
from .views import FollowMovieView, UpvoteDiscussionView, DownvoteDiscussionView
from .views import SearchResultsListView
from .views import CommentDetailView, CommentCreateView, CommentDeleteView, CommentEditView

urlpatterns = [
    path('follow/', FollowMovieView.as_view(), name ='follow'),
    path('<int:pk>/edit/', MovieEditView.as_view(), name='movie_edit'),
    path('<int:pk>/', MovieDetailView.as_view(), name='movie_detail'),
    path('<int:pk>/delete/', MovieDeleteView.as_view(), name='movie_delete'),
    path('new/', MovieCreateView.as_view(), name='movie_new'),
    path('request/', MovieRequestView.as_view(), name='movie_request'),
    path('request_list/<title>/<year>/', MovieRequestListView.as_view(), name='movie_request_list_year'),
    path('request_list/<title>/', MovieRequestListView.as_view(), name='movie_request_list'),
    path('list/', MovieListTitleView.as_view(), name='movie_list'),
    path('latest/', MovieListLatestView.as_view(), name='movie_list_latest'),
    path('search/', SearchResultsListView.as_view(), name='search_results'),
    path('', MovieFollowedTitleView.as_view(), name='movie_followed'),
    path('followedlatest/', MovieFollowedLatestView.as_view(), name='movie_followed_latest'),

    path('upvote_discussion/', UpvoteDiscussionView.as_view(), name ='upvote_discussion'),
    path('downvote_discussion/', DownvoteDiscussionView.as_view(), name ='downvote_discussion'),
    path('<movie_pk>/discussion/new/', DiscussionListViewNew.as_view(), name='discussion_list'),
    path('<movie_pk>/discussion/top/', DiscussionListViewTop.as_view(), name='discussion_list_top'),
    path('<movie_pk>/discussion/<int:discussion_pk>/', DiscussionDetailView.as_view(), name='discussion_detail'),
    path('<movie_pk>/discussion/<int:discussion_pk>/delete/', DiscussionDeleteView.as_view(), name='discussion_delete'),
    path('<movie_pk>/discussion/<discussion_pk>/edit/',DiscussionEditView.as_view(), name='discussion_edit'),
    path('<movie_pk>/discussion/new_discussion/', DiscussionCreateView.as_view(), name='discussion_new'),

    path('<movie_pk>/review/', ReviewListView.as_view(), name='review_list'),
    path('<movie_pk>/review/<int:review_pk>/', ReviewDetailView.as_view(), name='review_detail'),
    path('<movie_pk>/review/<int:review_pk>/delete/', ReviewDeleteView.as_view(), name='review_delete'),
    path('<movie_pk>/review/<review_pk>/edit/',ReviewEditView.as_view(), name='review_edit'),
    path('<movie_pk>/review/new/', ReviewCreateView.as_view(), name='review_new'),

    path('<movie_pk>/discussion/<discussion_pk>/comments/new/', CommentCreateView.as_view(), name='comment_new'),
    path('<movie_pk>/discussion/<discussion_pk>/comments/<comment_pk>/', CommentDetailView.as_view(), name='comment_detail'),
    path('<movie_pk>/discussion/<discussion_pk>/comments/<comment_pk>/delete/', CommentDeleteView.as_view(), name='comment_delete'),
    path('<movie_pk>/discussion/<discussion_pk>/comments/<comment_pk>/edit/', CommentEditView.as_view(), name='comment_edit'),
    

]