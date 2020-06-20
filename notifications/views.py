from django.shortcuts import render, redirect
from .models import Notification
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, View


class NotificationListView(LoginRequiredMixin, ListView):
    model = Notification
    template_name = 'notifications/notification_list.html'
    login_url = 'account_login'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['object_list'] = self.request.user.notifications.all().order_by('-date')
        return context

class NotificationClearView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        pk = request.POST.get("pk")
        obj = Notification.objects.get(pk=pk)
        user = self.request.user
        user.notifications.remove(obj)
        
        return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))

class NotificationClearAllView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        user = self.request.user
        user.notifications.clear()
        
        return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))