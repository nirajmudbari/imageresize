from django.urls import path

from . import views

urlpatterns = [
    path('', views.fetchandresize, name='fetchandresize'),
]
