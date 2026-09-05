from django.urls import path
from . import views

app_name = 'news'

urlpatterns = [
    path('', views.news_list, name='list'),
    path('<slug:slug>/', views.news_detail, name='detail'),
    path('category/<slug:slug>/', views.category_detail, name='category'),
    path('create/', views.news_create, name='create'),
    path('<slug:slug>/edit/', views.news_edit, name='edit'),
]
