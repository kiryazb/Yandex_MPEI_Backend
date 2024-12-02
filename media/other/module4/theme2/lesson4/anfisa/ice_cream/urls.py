from django.urls import path

from . import views

urlpatterns = [
    path('', views.ice_cream_list),
    path('<int:pk>/', views.ice_cream_detail),
]
