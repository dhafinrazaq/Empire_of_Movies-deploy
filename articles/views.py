from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DetailView, View, TemplateView
from django.views.generic.edit import UpdateView, DeleteView, CreateView
from django.urls import reverse_lazy, reverse
from django.shortcuts import get_object_or_404, redirect
from django.db.models import F, Count, Q
from django.contrib.auth import get_user_model

from .models import Movie, Discussion, Review, Comment
from notifications.models import Notification
from bot import telegram_bot_sendtext
from django.contrib import messages
from api import get_possible_movies

class SearchResultsListView(LoginRequiredMixin, TemplateView):
    template_name = 'search_result.html'
    login_url = 'account_login'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        query = self.request.GET.get('q')

        queryset = Movie.objects.none()
        if(self.request.GET.get("title")!= None):
            queryset |= Movie.objects.filter(Q(title__icontains=query))
        if(self.request.GET.get("year") !=None):
            queryset |= Movie.objects.filter(Q(year__icontains=query))
        if(self.request.GET.get("synopsis") !=None):
            queryset |= Movie.objects.filter(Q(synopsis__icontains=query))
        if(self.request.GET.get("stars") !=None):
            queryset |= Movie.objects.filter(Q(stars__icontains=query))
        if(self.request.GET.get("genre") !=None):
            queryset |= Movie.objects.filter(Q(genres__icontains=query))
        if(self.request.GET.get("keywords") !=None):
            queryset |= Movie.objects.filter(Q(keywords__icontains=query))

        context['movie_list'] = queryset
        context['discussion_list'] = Discussion.objects.filter(Q(title__icontains=query) | Q(body__icontains=query) | Q(author__username__icontains=query))
        context['review_list'] = Review.objects.filter(Q(title__icontains=query) | Q(body__icontains=query) | Q(author__username__icontains=query))
        return context

class MovieCreateView(LoginRequiredMixin, CreateView):
    model = Movie
    template_name = 'movies/movie_new.html'
    fields = ('title', 'synopsis')
    login_url = 'account_login'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class MovieRequestView(LoginRequiredMixin, TemplateView):
    template_name = 'movies/movie_request.html'
    login_url = 'account_login'

    def post(self, request, *args, **kwargs):
        #print(request.POST)
        title = request.POST.get('title')
        if (request.POST.get('year')):
            year = request.POST.get('year')
            possible_movies = get_possible_movies(title, year)
            if (possible_movies):
                return redirect(reverse('movie_request_list_year', args=[title, year]))
            else:
                messages.success(request, 'Movie request failed')
                return redirect(reverse("movie_request"))
        else:
            year = ""
            possible_movies = get_possible_movies(title, year)
            if (possible_movies):
                return redirect(reverse('movie_request_list', args=[title]))
            else: 
                messages.success(request, 'Movie request failed')
                return redirect(reverse("movie_request")) 

class MovieRequestListView(LoginRequiredMixin, TemplateView):
    template_name = 'movies/movie_request_list.html'
    login_url = 'account_login'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        title = self.kwargs.get('title')
        if (self.kwargs.get('year')):
            year = self.kwargs.get('year')
        else:
            year = ''
        possible_movies = get_possible_movies(title, year)
        context['possible_movies'] = possible_movies
        print(context['possible_movies'])
        return context

    def post(self, request, *args, **kwargs):
        id = request.POST.get('id')
        movie = Movie.create(id)
        if (Movie.objects.filter(title=movie.title).all().count() == 0):
            movie.save()
        return redirect(Movie.objects.get(title=movie.title))
        
        

class FollowMovieView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        #print(request.POST)
        MovietoFollow = request.POST.get("title")
        obj = Movie.objects.get(title=MovietoFollow)
        user = self.request.user
        if user in obj.follower.all():
            obj.follower.remove(user)
        else:
            obj.follower.add(user)
        
        return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))

class MovieDetailView(LoginRequiredMixin, DetailView):
    model = Movie
    template_name = 'movies/movie_detail.html'
    login_url = 'account_login'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_followed'] = self.request.user in Movie.objects.get(pk=self.kwargs.get('pk')).follower.all()
        context['is_author'] = self.request.user == Movie.objects.get(pk=self.kwargs.get('pk')).author
        return context


class MovieListView(LoginRequiredMixin, ListView):
    model = Movie
    template_name = 'movies/movie_list.html'
    login_url = 'account_login'

class MovieListTitleView(LoginRequiredMixin, ListView):
    model = Movie
    template_name = 'movies/movie_list.html'
    login_url = 'account_login'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['movie_list'] = Movie.objects.all().order_by('title')
        context['sort_by'] = 'alphabet'
        return context

class MovieListLatestView(LoginRequiredMixin, ListView):
    model = Movie
    template_name = 'movies/movie_list.html'
    login_url = 'account_login'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['movie_list'] = Movie.objects.all().order_by('-releaseDate')
        context['sort_by'] = 'latest'
        return context

class MovieFollowedView(LoginRequiredMixin, ListView):
    model = Movie
    template_name = 'movies/movie_followed.html'
    login_url = 'account_login'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['movie_followed'] = self.request.user.follows.all()
        return context

class MovieFollowedTitleView(LoginRequiredMixin, ListView):
    model = Movie
    template_name = 'movies/movie_followed.html'
    login_url = 'account_login'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['movie_followed'] = self.request.user.follows.all().order_by('title')
        context['sort_by'] = 'alphabet'
        return context

class MovieFollowedLatestView(LoginRequiredMixin, ListView):
    model = Movie
    template_name = 'movies/movie_followed.html'
    login_url = 'account_login'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['movie_followed'] = self.request.user.follows.all().order_by('-releaseDate')
        context['sort_by'] = 'latest'
        return context

class MovieEditView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Movie
    fields = ('synopsis',)
    template_name = 'movies/movie_edit.html'
    login_url = 'account_login'

    def test_func(self):
        obj = self.get_object()
        return obj.author == self.request.user


class MovieDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Movie
    template_name = 'movies/movie_delete.html'
    success_url = reverse_lazy('movie_list')
    login_url = 'account_login'

    def test_func(self):
        obj = self.get_object()
        return obj.author == self.request.user

############################################################################################################
class DiscussionDetailView(LoginRequiredMixin, DetailView):
    model = Discussion
    template_name = 'discussions/discussion_detail.html'
    login_url = 'account_login'

    def get_object(self):
        return Discussion.objects.get(pk=self.kwargs.get('discussion_pk'))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['movie_name'] = Movie.objects.get(pk=self.kwargs.get('movie_pk')).title
        context['discussion']= Discussion.objects.get(pk=self.kwargs.get('discussion_pk'))
        context['movie_pk'] = self.kwargs.get('movie_pk')
        context['discussion_name'] = Discussion.objects.get(pk=self.kwargs.get('discussion_pk')).title
        context['discussion_pk'] = self.kwargs.get('discussion_pk')
        context['voters_count'] = Discussion.objects.get(pk=self.kwargs.get('discussion_pk')).discussion_upvoter.all().count() \
            - Discussion.objects.get(pk=self.kwargs.get('discussion_pk')).discussion_downvoter.all().count()
        context['is_upvoter'] = self.request.user in Discussion.objects.get(pk=self.kwargs.get('discussion_pk')).discussion_upvoter.all()
        context['is_downvoter'] = self.request.user in Discussion.objects.get(pk=self.kwargs.get('discussion_pk')).discussion_downvoter.all()
        context['comment_list'] = Comment.objects.filter(discussion__pk=self.kwargs.get('discussion_pk')).order_by('-date')
        return context

class DiscussionCreateView(LoginRequiredMixin, CreateView):
    model = Discussion
    template_name = 'discussions/discussion_new.html'
    fields = ('title', 'body',) 
    login_url = 'account_login'

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.movie = get_object_or_404(Movie, 
                                                  id=self.kwargs.get('movie_pk'))
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['movie_name'] = Movie.objects.get(pk=self.kwargs.get('movie_pk')).title
        context['movie_pk'] = self.kwargs.get('movie_pk')
        return context

    def post(self, request, *args, **kwargs):
        #print(request.POST)
        super().post(request, *args, **kwargs)
        current_movie = Movie.objects.get(pk=self.kwargs.get('movie_pk'))
        all_followers = current_movie.all_followers()
        title = "New Discussion for"
        print(self.object.get_absolute_url())
        notification = Notification.create(title=title, movie=current_movie, inside=self.object)
        notification.save()
        for follower in all_followers:
            if (notification not in follower.notifications.all()):
                follower.notifications.add(notification)
            if (follower.chat_id):
                telegram_bot_sendtext(follower.chat_id, "New discussion for " + notification.movie_title + " with title " + notification.inside_title, "empire-of-movies.herokuapp.com" + notification.inside_link)
        
        return redirect(self.object)

class UpvoteDiscussionView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        #print(request.POST)
        DiscussionToVote = request.POST.get("title")
        obj = Discussion.objects.get(title=DiscussionToVote)
        user = self.request.user
        if user in obj.discussion_upvoter.all():
            obj.discussion_upvoter.remove(user)
        else:
            if user in obj.discussion_downvoter.all():
                obj.discussion_downvoter.remove(user)
            obj.discussion_upvoter.add(user)
        
        return redirect(obj)

class DownvoteDiscussionView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        #print(request.POST)
        DiscussionToVote = request.POST.get("title")
        obj = Discussion.objects.get(title=DiscussionToVote)
        user = self.request.user
        if user in obj.discussion_downvoter.all():
            obj.discussion_downvoter.remove(user)
        else:
            if user in obj.discussion_upvoter.all():
                obj.discussion_upvoter.remove(user)
            obj.discussion_downvoter.add(user)
        
        return redirect(obj)

class DiscussionDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Discussion
    template_name ='discussions/discussion_delete.html'
    success_url = reverse_lazy('movie_list')
    login_url = 'account_login'

    def test_func(self):
        obj = self.get_object()
        return obj.author == self.request.user

    def get_object(self):
        return Discussion.objects.get(pk=self.kwargs.get('discussion_pk'))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['movie_name'] = Movie.objects.get(pk=self.kwargs.get('movie_pk')).title
        context['movie_pk'] = self.kwargs.get('movie_pk')
        context['discussion_name'] = Discussion.objects.get(pk=self.kwargs.get('discussion_pk')).title
        context['discussion_pk'] = self.kwargs.get('discussion_pk')
        return context

class DiscussionEditView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Discussion
    fields =('body',)
    template_name = 'discussions/discussion_edit.html'
    success_url = reverse_lazy('movie_list')
    login_url ='account_login'

    def test_func(self):
        obj = self.get_object()
        return obj.author == self.request.user

    def get_object(self):
        return Discussion.objects.get(pk=self.kwargs.get('discussion_pk'))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['movie_name'] = Movie.objects.get(pk=self.kwargs.get('movie_pk')).title
        context['movie_pk'] = self.kwargs.get('movie_pk')
        context['discussion_name'] = Discussion.objects.get(pk=self.kwargs.get('discussion_pk')).title
        context['discussion_pk'] = self.kwargs.get('discussion_pk')
        return context

class DiscussionListViewTop(LoginRequiredMixin, ListView):
    model = Discussion
    template_name = 'discussions/discussion_list.html'
    login_url = 'account_login'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['object_list'] = Discussion.objects.filter(movie__pk=self.kwargs.get('movie_pk')).annotate(upvoter_count=Count('discussion_upvoter'), \
            downvoter_count=Count('discussion_downvoter')).order_by(F('downvoter_count') - F('upvoter_count'))
        context['movie_name'] = Movie.objects.get(pk=self.kwargs.get('movie_pk')).title
        context['movie_pk'] = self.kwargs.get('movie_pk')
        context['sort_by'] = 'top'
        return context

class DiscussionListViewNew(LoginRequiredMixin, ListView):
    model = Discussion
    template_name = 'discussions/discussion_list.html'
    login_url = 'account_login'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['object_list'] = Discussion.objects.filter(movie__pk=self.kwargs.get('movie_pk')).order_by('-date')
        context['movie_name'] = Movie.objects.get(pk=self.kwargs.get('movie_pk')).title
        context['movie_pk'] = self.kwargs.get('movie_pk')
        context['sort_by'] = 'new'
        return context

class ReviewDetailView(LoginRequiredMixin, DetailView):
    model = Review
    template_name = 'reviews/review_detail.html'
    login_url = 'account_login'

    def get_object(self):
        return Review.objects.get(pk=self.kwargs.get('review_pk'))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['movie_name'] = Movie.objects.get(pk=self.kwargs.get('movie_pk')).title
        context['review']= Review.objects.get(pk=self.kwargs.get('review_pk'))
        context['movie_pk'] = self.kwargs.get('movie_pk')
        context['review_name'] = Review.objects.get(pk=self.kwargs.get('review_pk')).title
        context['review_pk'] = self.kwargs.get('review_pk')
        return context

class ReviewCreateView(LoginRequiredMixin, CreateView):
    model = Review
    template_name = 'reviews/review_new.html'
    fields = ('title', 'body', 'rating',) 
    login_url = 'account_login'

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.movie = get_object_or_404(Movie, 
                                                  id=self.kwargs.get('movie_pk'))
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['movie_name'] = Movie.objects.get(pk=self.kwargs.get('movie_pk')).title
        context['movie_pk'] = self.kwargs.get('movie_pk')
        return context

    def post(self, request, *args, **kwargs):
        #print(request.POST)
        super().post(request, *args, **kwargs)
        current_movie = Movie.objects.get(pk=self.kwargs.get('movie_pk'))
        all_followers = current_movie.all_followers()
        title = "New Discussion for"
        print(self.object.get_absolute_url())
        notification = Notification.create(title=title, movie=current_movie, inside=self.object)
        notification.save()
        for follower in all_followers:
            if (notification not in follower.notifications.all()):
                follower.notifications.add(notification)
            if (follower.chat_id):
                telegram_bot_sendtext(follower.chat_id, "New review for " + notification.movie_title + " with title " + notification.inside_title, "empire-of-movies.herokuapp.com0" + notification.inside_link)
        
        return redirect(self.object)

class ReviewDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Review
    template_name ='reviews/review_delete.html'
    success_url = reverse_lazy('movie_list')
    login_url = 'account_login'

    def test_func(self):
        obj = self.get_object()
        return obj.author == self.request.user

    def get_object(self):
        return Review.objects.get(pk=self.kwargs.get('review_pk'))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['review']=Review.objects.get(pk=self.kwargs.get('review_pk'))
        context['movie_name'] = Movie.objects.get(pk=self.kwargs.get('movie_pk')).title
        context['movie_pk'] = self.kwargs.get('movie_pk')
        context['review_name'] = Review.objects.get(pk=self.kwargs.get('review_pk')).title
        context['review_pk'] = self.kwargs.get('review_pk')
        return context

class ReviewEditView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Review
    fields =('body',)
    template_name = 'reviews/review_edit.html'
    success_url = reverse_lazy('movie_list')
    login_url ='account_login'

    def test_func(self):
        obj = self.get_object()
        return obj.author == self.request.user

    def get_object(self):
        return Review.objects.get(pk=self.kwargs.get('review_pk'))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['review'] = Review.objects.get(pk=self.kwargs.get('review_pk'))
        context['movie_name'] = Movie.objects.get(pk=self.kwargs.get('movie_pk')).title
        context['movie_pk'] = self.kwargs.get('movie_pk')
        context['review_name'] = Review.objects.get(pk=self.kwargs.get('review_pk')).title
        context['review_pk'] = self.kwargs.get('review_pk')
        return context

class ReviewListView(LoginRequiredMixin, ListView):
    model = Review
    template_name = 'reviews/review_list.html'
    login_url = 'account_login'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['object_list'] = Review.objects.filter(movie__pk=self.kwargs.get('movie_pk'))
        context['movie_name'] = Movie.objects.get(pk=self.kwargs.get('movie_pk')).title
        context['movie_pk'] = self.kwargs.get('movie_pk')
        return context

################################################################################################################

class CommentDetailView(LoginRequiredMixin, DetailView):
    model = Comment
    template_name = 'comment/comment_detail.html'
    login_url = 'account_login'

    def get_object(self):
        return Comment.objects.get(pk=self.kwargs.get('comment_pk'))

    def get_context_data(self, **kwargs):
        print(self.kwargs)
        context = super().get_context_data(**kwargs)
        context['movie_name'] = Movie.objects.get(pk=self.kwargs.get('movie_pk')).title
        context['discussion']= Discussion.objects.get(pk=self.kwargs.get('discussion_pk'))
        context['movie_pk'] = self.kwargs.get('movie_pk')
        context['discussion_name'] = Discussion.objects.get(pk=self.kwargs.get('discussion_pk')).title
        context['discussion_pk'] = self.kwargs.get('discussion_pk')
        return context

class CommentCreateView(LoginRequiredMixin, TemplateView):
    model = Comment
    login_url = 'account_login'

    def post(self, request, *args, **kwargs):
        User = get_user_model()
        title = request.POST.get('title')
        discussion = Discussion.objects.get(pk=request.POST.get('discussion_id'))
        author = self.request.user
        comment = Comment.create(title, author, discussion)
        comment.save()
        return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))

class CommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Comment
    template_name ='comment/comment_delete.html'
    success_url = reverse_lazy('movie_list')
    login_url = 'account_login'

    def test_func(self):
        obj = self.get_object()
        return obj.author == self.request.user

    def get_object(self):
        return Comment.objects.get(pk=self.kwargs.get('comment_pk'))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['movie_name'] = Movie.objects.get(pk=self.kwargs.get('movie_pk')).title
        context['movie_pk'] = self.kwargs.get('movie_pk')
        context['discussion_name'] = Discussion.objects.get(pk=self.kwargs.get('discussion_pk')).title
        context['discussion_pk'] = self.kwargs.get('discussion_pk')
        return context

class CommentEditView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Comment
    fields =('title',)
    template_name = 'comment/comment_edit.html'
    login_url ='account_login'

    def test_func(self):
        obj = self.get_object()
        return obj.author == self.request.user

    def get_object(self):
        return Comment.objects.get(pk=self.kwargs.get('comment_pk'))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['movie_name'] = Movie.objects.get(pk=self.kwargs.get('movie_pk')).title
        context['movie_pk'] = self.kwargs.get('movie_pk')
        context['discussion_name'] = Discussion.objects.get(pk=self.kwargs.get('discussion_pk')).title
        context['discussion_pk'] = self.kwargs.get('discussion_pk')
        return context