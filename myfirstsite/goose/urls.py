from django.urls import path, include
from . import views

app_name = 'goose'

urlpatterns = [
    path('', views.banderogoose, name='banderogoose'),
]
