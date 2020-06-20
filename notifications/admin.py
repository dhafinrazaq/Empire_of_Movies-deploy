from django.contrib import admin
from .models import Notification
from django.contrib.auth import get_user_model

# Register your models here.
class NotifiedInline(admin.TabularInline):
    User = get_user_model()
    model = User.notifications.through

class NotificationAdmin(admin.ModelAdmin): # new 
    inlines = [
        NotifiedInline,
    ]

admin.site.register(Notification, NotificationAdmin)