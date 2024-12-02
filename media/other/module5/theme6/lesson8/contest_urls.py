from django.urls import path

from . import views

app_name = 'contest'

urlpatterns = [
    path('', views.proposal, name='create'),
    path('list/', views.proposal_list, name='list'),
    path('<int:pk>/edit/', views.proposal, name='edit'),
    path('<int:pk>/delete/', views.delete_proposal, name='delete'),
]
