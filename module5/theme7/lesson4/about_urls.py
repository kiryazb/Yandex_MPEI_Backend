from django.urls import path

from . import views


app_name = 'about'

urlpatterns = [
    path('', views.Description.as_view(), name='description'),
]
