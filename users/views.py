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

class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'account/profile_view.html'
    login_url = 'account_login'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        print("kwargs======" + str(self.kwargs))
        User = get_user_model()
        context['user'] = User.objects.get(username=self.kwargs.get('username'))
        context['discussions'] = Discussion.objects.filter(author=context['user'])
        context['reviews'] = Review.objects.filter(author=context['user'])
        context['comments'] = Comment.objects.filter(author=context['user'])
        context['following'] = context['user'].follows
        return context

# class SocialLoginView(View):
#     pass