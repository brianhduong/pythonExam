from django.conf.urls import url
from . import views           # This line is new!

urlpatterns = [
	url(r'^$', views.index),
	url(r'^login$', views.login),
	url(r'^register$', views.register),
	url(r'^home$', views.home),
	url(r'^addQuote$', views.addQuote),
	url(r'^addToFavorites/(?P<id>\d+)$', views.addToFavorites),
	url(r'^removeFave/(?P<id>\d+)$', views.removeFavorite),
	url(r'^userPage/(?P<id>\d+)$', views.userPage),
	url(r'^logout$', views.logout)
]