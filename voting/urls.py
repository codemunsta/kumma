from django.urls import path
from . import views


urlpatterns = [
    path('vote', views.vote_page, name='votes'),
    path('confirmed', views.confirmation, name='confirmed')
]
