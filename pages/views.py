from django.views.generic import TemplateView
from articles.models import Discussion, Review
from django.contrib.auth.mixins import LoginRequiredMixin

class HomePageDiscussion(TemplateView):
    template_name = 'home/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['discussion_list'] = Discussion.objects.all().order_by('-date')
        return context

class HomePageReview(TemplateView):
    template_name = 'home/home_review.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['review_list'] = Review.objects.all().order_by('-date')
        return context

class HomePageLoginDiscussion(LoginRequiredMixin, TemplateView):
    template_name = 'home/home_login_discussion.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        discussion_list=[]
        for movie in user.follows.all():
            discussion_list.extend(list(movie.discussion.all()))
        context['discussion_list'] = sorted(discussion_list, key = lambda x:x.date, reverse=True)
        return context

class HomePageLoginReview(LoginRequiredMixin, TemplateView):
    template_name = 'home/home_login_review.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        review_list=[]
        for movie in user.follows.all():
            review_list.extend(list(movie.review.all()))
        context['review_list'] = sorted(review_list, key = lambda x:x.date, reverse=True)
        return context

    


class PrivacyPolicyView(TemplateView):
    template_name = 'privacy_policy.html'