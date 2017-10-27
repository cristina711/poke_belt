from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^login$', views.login),
    url(r'^register$', views.register),
    url(r'^success$', views.success),
    url(r'^poketable$', views.poke),
    url(r'poketable$', views.poketable, name="poketable"),
	url(r'logout$', views.logout, name="logout"),
	url(r'^pokes/(?P<user_id>\d+)/$', views.pokeaction, name="pokeaction"),
]