from django.contrib import admin

# Register your models here.
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser
from articles.models import Movie
from notifications.models import Notification
from report.models import Report

class MovieInline(admin.TabularInline):
    model = CustomUser.follows.through
    extra = 0

class DiscussionUpvotesInline(admin.TabularInline):
    model = CustomUser.upvotes_discussion.through
    extra = 0

class DiscussionDownvotesInline(admin.TabularInline):
    model = CustomUser.downvotes_discussion.through
    extra = 0

class NotificationsInline(admin.TabularInline):
    model = CustomUser.notifications.through
    extra = 0

class ReportInline(admin.TabularInline):
    model = Report
    fk_name = 'reported'
    extra = 0

class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display=['email', 'username','is_staff', 'telegram_id',]
    fieldsets = (
        (None, {
            'fields': ('username', 'email', 'telegram_id')
        }),
        )
    inlines = [
        MovieInline, DiscussionUpvotesInline, DiscussionDownvotesInline, NotificationsInline, ReportInline, 
    ]

admin.site.register(CustomUser, CustomUserAdmin)