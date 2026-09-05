from django.urls import path
from . import views

app_name = 'leadership'

urlpatterns = [
    path('', views.leadership_list, name='list'),
    path('<slug:slug>/', views.leader_detail, name='detail'),
]
