from django.urls import path
from . import views
from . import member_views

app_name = 'appointments'

urlpatterns = [
    # Admin URLs
    path('', views.appointment_list, name='list'),
    path('create/', views.appointment_create, name='create'),
    path('<int:appointment_id>/', views.appointment_detail, name='detail'),
    path('<int:appointment_id>/preview/', views.appointment_letter_preview, name='preview'),
    path('<int:appointment_id>/pdf/', views.appointment_letter_pdf, name='pdf'),
    path('<int:appointment_id>/delete/', views.appointment_delete, name='delete'),
    
    # Member URLs
    path('my/', member_views.my_appointments, name='my_appointments'),
    path('my/<int:appointment_id>/', member_views.my_appointment_detail, name='my_appointment_detail'),
    path('my/<int:appointment_id>/pdf/', member_views.my_appointment_pdf, name='my_appointment_pdf'),
]
