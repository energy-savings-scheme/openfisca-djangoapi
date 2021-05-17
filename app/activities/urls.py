from django.urls import path
from activities.views import ActivityList

urlpatterns = [
    path('', ActivityList.as_view(), name='index'),
]
