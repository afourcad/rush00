from django.urls import path, re_path

from . import views

app_name='moviemons'
urlpatterns = [
    re_path('', views.index)
]