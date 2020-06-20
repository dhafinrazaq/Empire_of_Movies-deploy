from django.contrib import admin

from .models import Movie, Discussion, Review, Comment
from report.models import Report
from django.contrib.auth import get_user_model


class MovieFollowersInline(admin.TabularInline):
    User = get_user_model()
    model = User.follows.through

class DiscussionDownvotersInline(admin.TabularInline):
    User = get_user_model()
    model = User.downvotes_discussion.through
    extra = 0

class DiscussionUpvotersInline(admin.TabularInline):
    User = get_user_model()
    model = User.upvotes_discussion.through
    extra = 0

class CommentsInline(admin.TabularInline):
    model = Comment
    extra = 0

class DiscussionInline(admin.TabularInline): # new 
    model = Discussion
    extra = 0

class ReviewInline(admin.TabularInline): # new 
    model = Review
    extra = 0

class DiscussionReportInline(admin.TabularInline):
    model = Report
    extra = 0

class ReviewReportInline(admin.TabularInline):
    model = Report
    extra = 0

class CommentReportInline(admin.TabularInline):
    model = Report
    extra = 0

class MovieAdmin(admin.ModelAdmin): # new 
    inlines = [
        MovieFollowersInline,
        DiscussionInline,
        ReviewInline,
    ]


class DiscussionAdmin(admin.ModelAdmin): # new 
    inlines = [
        DiscussionUpvotersInline,
        DiscussionDownvotersInline,
        CommentsInline,
        DiscussionReportInline,
    ]

class ReviewAdmin(admin.ModelAdmin): # new 
    inlines = [
        ReviewReportInline,
    ]

class CommentAdmin(admin.ModelAdmin): # new 
    inlines = [
        CommentReportInline,
    ]
    
    
admin.site.register(Movie, MovieAdmin) # new 
admin.site.register(Review, ReviewAdmin)
admin.site.register(Discussion, DiscussionAdmin)
admin.site.register(Comment, CommentAdmin)