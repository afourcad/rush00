from django.conf.urls import url
from django.urls import path

from . import views

app_name='moviemons'
urlpatterns = [
	url(r'^options/load_game', views.OptionsLoad),
	url(r'^options/save_game', views.OptionsSave),
	url(r'^battle/(?P<moviemon_id>[-\w]+)/$', views.Battle),
	url(r'^worldmap', views.Worldmap),
	url(r'^options', views.Options),
	url(r'^moviedex/(?P<moviemon_id>[-\w]+)$', views.MoviedexDetail),
	url(r'^moviedex', views.Moviedex),
	url(r'^$', views.new),
]