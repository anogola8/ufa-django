from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Count, Sum, Q
from django.utils import timezone
from django.contrib import messages
from datetime import datetime, timedelta

# Import all models
from members.models import Member
from events.models import Event, EventRegistration
from news.models import News
from gallery.models import Album, Photo, Video
from projects.models import Project
from leadership.models import Leader
from appointments.models import Appointment


@login_required
def member_dashboard(request):
    # Get member profile
    try:
        member = request.user.member_profile
    except:
        member = None
        return render(request, 'dashboard/member.html', {
            'member': None,
            'upcoming_events': [],
            'past_events': [],
            'notifications': [],
            'total_events_attended': 0,
            'pending_registrations': 0,
            'total_appointments': 0,
        })
    
    # Get upcoming events
    upcoming_events = EventRegistration.objects.filter(
        member=member,
        event__start_date__gte=timezone.now(),
        status__in=['confirmed', 'pending']
    ).order_by('event__start_date')[:5]
    
    # Get past events
    past_events = EventRegistration.objects.filter(
        member=member,
        event__start_date__lt=timezone.now()
    ).order_by('-event__start_date')[:5]
    
    # Get notifications (placeholder)
    notifications = []
    
    # Counts
    total_events_attended = EventRegistration.objects.filter(
        member=member,
        status='attended'
    ).count()
    
    pending_registrations = EventRegistration.objects.filter(
        member=member,
        status='pending'
    ).count()
    
    total_appointments = Appointment.objects.filter(member=member).count()
    
    context = {
        'member': member,
        'upcoming_events': upcoming_events,
        'past_events': past_events,
        'notifications': notifications,
        'total_events_attended': total_events_attended,
        'pending_registrations': pending_registrations,
        'total_appointments': total_appointments,
    }
    return render(request, 'dashboard/member.html', context)


@staff_member_required
def admin_dashboard(request):
    # Admin dashboard - for staff only
    context = {
        'total_members': Member.objects.count(),
        'pending_members': Member.objects.filter(membership_status='pending').count(),
        'active_members': Member.objects.filter(membership_status='active').count(),
        'total_events': Event.objects.count(),
        'upcoming_events': Event.objects.filter(start_date__gte=timezone.now(), status='published').count(),
        'total_news': News.objects.count(),
        'published_news': News.objects.filter(status='published').count(),
        'total_projects': Project.objects.count(),
        'active_projects': Project.objects.filter(status__in=['planning', 'ongoing']).count(),
        'completed_projects': Project.objects.filter(status='completed').count(),
        'total_albums': Album.objects.count(),
        'total_photos': Photo.objects.count(),
        'total_videos': Video.objects.count(),
        'total_leaders': Leader.objects.count(),
        'active_leaders': Leader.objects.filter(is_active=True).count(),
        'total_appointments': Appointment.objects.count(),
        'today': timezone.now(),
    }
    return render(request, 'dashboard/admin_dashboard.html', context)


@staff_member_required
def analytics_dashboard(request):
    # Analytics dashboard - for staff only
    six_months_ago = timezone.now() - timedelta(days=180)
    
    # Member growth
    member_growth = Member.objects.filter(joined_date__gte=six_months_ago).extra(
        {'month': "strftime('%%Y-%%m', joined_date)"}
    ).values('month').annotate(count=Count('id')).order_by('month')
    
    # Membership distribution
    membership_distribution = Member.objects.values('membership_type').annotate(
        count=Count('id')
    )
    
    # Event participation
    event_participation = Event.objects.filter(start_date__gte=six_months_ago).values('event_type').annotate(
        total_registrations=Count('registrations')
    ).order_by('-total_registrations')
    
    # Project status distribution
    project_status = Project.objects.values('status').annotate(
        count=Count('id')
    )
    
    # Monthly trends
    monthly_stats = {
        'members': list(member_growth),
        'events': list(Event.objects.filter(created_at__gte=six_months_ago).extra(
            {'month': "strftime('%%Y-%%m', created_at)"}
        ).values('month').annotate(count=Count('id')).order_by('month')),
        'registrations': list(EventRegistration.objects.filter(registration_date__gte=six_months_ago).extra(
            {'month': "strftime('%%Y-%%m', registration_date)"}
        ).values('month').annotate(count=Count('id')).order_by('month')),
    }
    
    context = {
        'member_growth': list(member_growth),
        'membership_distribution': list(membership_distribution),
        'event_participation': list(event_participation),
        'project_status': list(project_status),
        'monthly_stats': monthly_stats,
        'total_members': Member.objects.count(),
        'total_events': Event.objects.filter(status='published').count(),
        'total_projects': Project.objects.count(),
        'total_registrations': EventRegistration.objects.count(),
    }
    return render(request, 'dashboard/analytics.html', context)


@login_required
def executive_dashboard(request):
    # Alias for admin_dashboard (for backward compatibility)
    return admin_dashboard(request)


@staff_member_required
def reports_dashboard(request):
    # Reports dashboard - for staff only
    from reports.models import Report, ReportTemplate
    
    context = {
        'templates': ReportTemplate.objects.filter(is_active=True) if hasattr(ReportTemplate, 'objects') else [],
        'recent_reports': Report.objects.order_by('-generated_at')[:10] if hasattr(Report, 'objects') else [],
        'report_types': ReportTemplate.TEMPLATE_TYPES if hasattr(ReportTemplate, 'TEMPLATE_TYPES') else [],
    }
    return render(request, 'dashboard/reports.html', context)


@staff_member_required
def dashboard_stats_api(request):
    # API endpoint for dashboard statistics
    import json
    from django.http import JsonResponse
    
    data = {
        'total_members': Member.objects.count(),
        'active_members': Member.objects.filter(membership_status='active').count(),
        'total_events': Event.objects.filter(status='published').count(),
        'upcoming_events': Event.objects.filter(start_date__gte=timezone.now(), status='published').count(),
        'total_projects': Project.objects.filter(status__in=['planning', 'ongoing']).count(),
        'total_news': News.objects.filter(status='published').count(),
        'total_appointments': Appointment.objects.count(),
    }
    return JsonResponse(data)


@staff_member_required
def generate_report(request, template_id):
    # Generate a specific report
    import json
    from django.http import JsonResponse
    from reports.models import ReportTemplate, Report
    
    try:
        template = get_object_or_404(ReportTemplate, id=template_id)
    except:
        return JsonResponse({'error': 'Template not found'}, status=404)
    
    report = Report.objects.create(
        template=template,
        title=f"{template.name} - {timezone.now().strftime('%Y-%m-%d')}",
        parameters=request.GET.dict(),
        status='ready',
        generated_by=request.user,
    )
    
    return JsonResponse({
        'id': report.id,
        'title': report.title,
        'generated_at': report.generated_at,
        'message': 'Report generated successfully'
    })
