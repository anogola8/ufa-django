from django.urls import path
from . import views

app_name = 'events'

urlpatterns = [
    path('', views.event_list, name='list'),
    path('<slug:slug>/', views.event_detail, name='detail'),
    path('register/<int:event_id>/', views.register_event, name='register'),
    path('my-registrations/', views.my_registrations, name='my_registrations'),
    path('cancel/<int:registration_id>/', views.cancel_registration, name='cancel'),
]
