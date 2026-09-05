from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.utils import timezone
from appointments.models import Appointment
from members.models import Member

@login_required
def my_appointments(request):
    'View all appointments for the logged-in user'
    try:
        member = request.user.member_profile
        appointments = Appointment.objects.filter(member=member).order_by('-created_at')
    except:
        member = None
        appointments = []
    
    context = {
        'member': member,
        'appointments': appointments,
    }
    return render(request, 'appointments/my_appointments.html', context)

@login_required
def my_appointment_detail(request, appointment_id):
    'View a specific appointment letter for the logged-in user'
    try:
        member = request.user.member_profile
        appointment = get_object_or_404(Appointment, id=appointment_id, member=member)
    except:
        return redirect('appointments:my_appointments')
    
    context = {
        'appointment': appointment,
        'today': timezone.now(),
    }
    return render(request, 'appointments/letter_template.html', context)

@login_required
def my_appointment_pdf(request, appointment_id):
    'Download appointment letter as PDF (for members)'
    try:
        member = request.user.member_profile
        appointment = get_object_or_404(Appointment, id=appointment_id, member=member)
    except:
        return redirect('appointments:my_appointments')
    
    context = {
        'appointment': appointment,
        'today': timezone.now(),
    }
    return render(request, 'appointments/letter_template.html', context)
