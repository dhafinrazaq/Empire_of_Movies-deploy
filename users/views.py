from django.urls import reverse_lazy
from django.views.generic import TemplateView
from django.views.generic import UpdateView, View
from .forms import CustomUserCreationForm
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
import hashlib
import datetime
from .forms import CustomUserChangeForm
from articles.models import Discussion, Review, Comment
from django.shortcuts import redirect
from threadedcomments.models import ThreadedComment

class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = get_user_model()
    form_class = CustomUserChangeForm
    # fields = ('username', 'email', )
    template_name = 'account/profile_update.html'
    success_url = reverse_lazy('home')
    login_url ='account_login'

    def get_object(self):
        return self.request.user

class TelegramOTPView(LoginRequiredMixin, TemplateView):
    template_name = 'account/telegram_otp.html'
    login_url ='account_login'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        current_date = datetime.datetime.now()
        current_date_string = str(current_date.year) + str(current_date.month) + str(current_date.day) \
        + str(current_date.hour)
        # context['OTP'] = int(hashlib.sha256((chat_date_string + self.request.username).encode('utf-8')).hexdigest(), 16) % 10**8
        self.request.user.OTP = int(hashlib.sha256((current_date_string + self.request.user.username).encode('utf-8')).hexdigest(), 16) % 10**8
        self.request.user.save()
        context['OTP'] = self.request.user.OTP
        return context

class ProfileFollowingView(LoginRequiredMixin, TemplateView):
    template_name = 'account/profile_view_following.html'
    login_url = 'account_login'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        User = get_user_model()
        context['user_view'] = User.objects.get(username=self.kwargs.get('username'))
        context['following'] = context['user_view'].follows.all()
        return context

class ProfileDiscussionView(LoginRequiredMixin, TemplateView):
    template_name = 'account/profile_view_discussion.html'
    login_url = 'account_login'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        User = get_user_model()
        context['user_view'] = User.objects.get(username=self.kwargs.get('username'))
        context['discussions'] = Discussion.objects.filter(author=context['user_view'])
        return context

class ProfileReviewView(LoginRequiredMixin, TemplateView):
    template_name = 'account/profile_view_review.html'
    login_url = 'account_login'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        User = get_user_model()
        context['user_view'] = User.objects.get(username=self.kwargs.get('username'))
        context['reviews'] = Review.objects.filter(author=context['user_view'])
        return context

class ProfileCommentView(LoginRequiredMixin, TemplateView):
    template_name = 'account/profile_view_comment.html'
    login_url = 'account_login'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        User = get_user_model()
        context['user_view'] = User.objects.get(username=self.kwargs.get('username'))
        context['comments'] = ThreadedComment.objects.filter(user_name=context['user_view'].username).filter(is_removed=False)
        return context

class TelegramDisconnectView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        #print(request.POST)
        user = self.request.user
        user.telegram_id = None
        user.chat_id = None
        user.save()
        return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))

