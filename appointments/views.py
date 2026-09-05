from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from django.utils import timezone
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.conf import settings
import os
import io
import sys
from .models import Appointment
from .forms import AppointmentForm

# Only use ReportLab (pure Python, works on all platforms)
try:
    from reportlab.lib.pagesizes import letter, A4
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, PageBreak
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.units import inch, cm
    from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
    from reportlab.lib import colors
    from reportlab.pdfgen import canvas
    REPORTLAB_AVAILABLE = True
except ImportError:
    REPORTLAB_AVAILABLE = False


@staff_member_required
def appointment_list(request):
    'View all appointments'
    appointments = Appointment.objects.all().order_by('-created_at')
    context = {'appointments': appointments}
    return render(request, 'dashboard/appointments/list.html', context)


@staff_member_required
def appointment_create(request):
    'Create a new appointment'
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            appointment = form.save(commit=False)
            appointment.approved_by = request.user
            appointment.approved_date = timezone.now()
            appointment.status = 'approved'
            appointment.save()

            # Generate the letter content
            appointment.letter_content = generate_letter_content(appointment)
            appointment.save()

            messages.success(request, f'Appointment letter created for {appointment.member.full_name}!')
            return redirect('appointments:detail', appointment.id)
    else:
        form = AppointmentForm()

    context = {'form': form, 'title': 'Create Appointment'}
    return render(request, 'dashboard/appointments/create.html', context)


@staff_member_required
def appointment_detail(request, appointment_id):
    'View appointment letter'
    appointment = get_object_or_404(Appointment, id=appointment_id)
    context = {'appointment': appointment}
    return render(request, 'dashboard/appointments/detail.html', context)


@staff_member_required
def appointment_letter_pdf(request, appointment_id):
    'Generate clean PDF of appointment letter'
    appointment = get_object_or_404(Appointment, id=appointment_id)
    
    # Return the HTML for printing (browser will handle PDF)
    context = {
        'appointment': appointment,
        'today': timezone.now(),
    }
    return render(request, 'appointments/letter_template.html', context)


@staff_member_required
def appointment_letter_preview(request, appointment_id):
    'Preview the appointment letter'
    appointment = get_object_or_404(Appointment, id=appointment_id)
    context = {
        'appointment': appointment,
        'today': timezone.now(),
    }
    return render(request, 'appointments/letter_template.html', context)


@staff_member_required
def appointment_delete(request, appointment_id):
    'Delete an appointment'
    appointment = get_object_or_404(Appointment, id=appointment_id)
    if request.method == 'POST':
        appointment.delete()
        messages.success(request, 'Appointment deleted successfully!')
        return redirect('appointments:list')
    return render(request, 'dashboard/appointments/delete.html', {'appointment': appointment})


def generate_letter_content(appointment):
    'Generate the letter content based on the appointment'
    position_display = appointment.get_position_display()
    first_name = appointment.member.full_name.split()[0] if appointment.member.full_name else 'Sir/Madam'

    letter = f"""
UNIQUE FOCUS ASSOCIATION (UFA)
"Unite and Rise - Together We Build"
Nairobi, Kenya
Tel: 07977551423

Date: {appointment.appointment_date.strftime('%d %B %Y')}

To: {appointment.member.full_name}
{appointment.county or 'National'} County, Kenya

RE: APPOINTMENT AS {position_display.upper()} - {appointment.county or 'NATIONAL'} COUNTY

Dear {first_name},

On behalf of the National Executive Council (NEC) and the leadership of Unique Focus Association (UFA), we are pleased to formally appoint you as the {position_display} for {appointment.county or 'National'} County.

Following the vetting process conducted by the duly constituted Vetting Committee, your application and qualifications were carefully reviewed. The Committee unanimously agreed to approve your appointment, having found you suitable to provide leadership and advance the vision, mission, and objectives of Unique Focus Association (UFA) within {appointment.county or 'the National'} County.

In this capacity, you will be responsible for:
• Providing strategic leadership to the County leadership team
• Coordinating and supervising county and ward officials
• Overseeing the implementation of UFA programs and activities
• Promoting membership recruitment, civic engagement, and organizational growth
• Ensuring that all county operations are conducted in accordance with the Constitution, policies, and directives of Unique Focus Association (UFA).

Your appointment takes effect from {appointment.effective_date.strftime('%d %B %Y')} and shall be governed by the Constitution of Unique Focus Association (UFA) and any applicable policies, regulations, or resolutions of the National Executive Council. You are expected to uphold the highest standards of integrity, accountability, discipline, and commitment in the discharge of your duties.

We are confident that your leadership will contribute significantly to strengthening UFA's presence and impact in {appointment.county or 'the National'} County and to advancing our collective goals of national unity, good governance, community empowerment, and sustainable development.

Congratulations on your appointment, and we wish you every success in your new role.

Yours faithfully,

Dericks Omondi
National Chairperson
Unique Focus Association (UFA)

Reference: {appointment.letter_reference}
"""
    return letter
