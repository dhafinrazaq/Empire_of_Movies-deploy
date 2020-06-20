from django.urls import path,include
from .views import NotificationListView, NotificationClearView, NotificationClearAllView

urlpatterns = [
    path('list/', NotificationListView.as_view(), name='notification_list'),
    path('clear/', NotificationClearView.as_view(), name='notification_clear'),
    path('clear_all/', NotificationClearAllView.as_view(), name='notification_clear_all'),
    # path('notify/', NotificationNotifyView.as_view(), name='notify'),
]