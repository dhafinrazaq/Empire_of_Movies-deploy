from django.contrib import admin
from django.urls import path,include

from .views import ReportFormView

urlpatterns = [
    path('', ReportFormView.as_view(), name='report'),
]
