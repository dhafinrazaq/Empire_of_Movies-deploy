from django.shortcuts import render
from django.views.generic import TemplateView, CreateView
from django.shortcuts import reverse, redirect
from .models import Report
from articles.models import Discussion, Review, Comment
from threadedcomments.models import ThreadedComment
from django.contrib.auth import get_user_model
from django.urls import reverse_lazy, reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from notifications.models import Notification

class ReportFormView(LoginRequiredMixin, TemplateView):
    model = Report
    success_url = reverse_lazy('home')
    login_url ='account_login'

    def post(self, request, *args, **kwargs):
        User = get_user_model()
        short_reason = request.POST.get('short_reason')
        long_reason = request.POST.get('long_reason')
        reported =  User.objects.get(username=request.POST.get('reported_id'))
        reporter = self.request.user
        discussion = None
        review = None
        comment = None
        if(request.POST.get('discussion_id')):
            discussion = Discussion.objects.get(pk=request.POST.get('discussion_id'))
        elif (request.POST.get('review_id')):
            review = Review.objects.get(pk=request.POST.get('review_id'))
        elif (request.POST.get('comment_id')):
            comment = ThreadedComment.objects.get(pk=request.POST.get('comment_id'))
        report = Report.create(reported, reporter, short_reason, long_reason, discussion, review, comment)
        report.save()
        if (reported.reported.all().count() % 5 == 0):
            notification = Notification.create_title('Your account have been suspected for inappropriate behaviour')
            notification.save()
            reported.notifications.add(notification)
        return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))