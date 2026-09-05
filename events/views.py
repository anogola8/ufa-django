from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from django.utils import timezone
from django.http import Http404
from .models import Event, EventRegistration
from members.models import Member

def event_list(request):
    """View all events - shows ALL published events"""
    now = timezone.now()
    
    # Get ALL published events with valid slugs
    all_published = Event.objects.filter(status='published').exclude(slug='').order_by('start_date')
    
    # Separate upcoming and past
    upcoming_events = all_published.filter(start_date__gte=now)
    past_events = all_published.filter(start_date__lt=now)
    
    context = {
        'upcoming_events': upcoming_events,
        'past_events': past_events,
        'now': now,
    }
    return render(request, 'events/list.html', context)

def event_detail(request, slug):
    """View single event"""
    try:
        event = get_object_or_404(Event, slug=slug, status='published')
    except Http404:
        # If event not found with slug, try to find by title
        event = Event.objects.filter(status='published').first()
        if event:
            return redirect('events:detail', slug=event.slug)
        raise
    
    context = {
        'event': event,
    }
    return render(request, 'events/detail.html', context)

@login_required
def register_event(request, event_id):
    """Register for an event"""
    event = get_object_or_404(Event, id=event_id)
    
    # Check if user has a member profile
    try:
        member = request.user.member_profile
    except:
        messages.error(request, 'Please complete your member profile first.')
        return redirect('events:detail', slug=event.slug)
    
    # Check if member is active
    if member.membership_status != 'active':
        messages.error(request, 'Your membership is not active. Please renew your membership.')
        return redirect('events:detail', slug=event.slug)
    
    # Check if event is full
    if event.is_full:
        messages.error(request, 'This event is already full.')
        return redirect('events:detail', slug=event.slug)
    
    # Check if already registered
    registration = EventRegistration.objects.filter(event=event, member=member).first()
    if registration:
        if registration.status == 'confirmed':
            messages.info(request, 'You are already registered for this event.')
        elif registration.status == 'pending':
            messages.info(request, 'Your registration is pending confirmation.')
        return redirect('events:detail', slug=event.slug)
    
    # Create registration
    registration = EventRegistration.objects.create(
        event=event,
        member=member,
        status='pending'
    )
    
    event.current_participants += 1
    event.save()
    
    messages.success(request, f'You have successfully registered for {event.title}!')
    return redirect('events:detail', slug=event.slug)

@login_required
def my_registrations(request):
    """View user's registrations"""
    try:
        member = request.user.member_profile
        registrations = EventRegistration.objects.filter(member=member).order_by('-registration_date')
    except:
        registrations = []
    
    context = {
        'registrations': registrations,
    }
    return render(request, 'events/my_registrations.html', context)

@login_required
def cancel_registration(request, registration_id):
    """Cancel event registration"""
    registration = get_object_or_404(EventRegistration, id=registration_id, member__user=request.user)
    
    if registration.status == 'cancelled':
        messages.info(request, 'This registration is already cancelled.')
        return redirect('events:my_registrations')
    
    if registration.event.start_date < timezone.now():
        messages.error(request, 'Cannot cancel registration for past events.')
        return redirect('events:my_registrations')
    
    registration.status = 'cancelled'
    registration.save()
    
    registration.event.current_participants -= 1
    registration.event.save()
    
    messages.success(request, 'Registration cancelled successfully.')
    return redirect('events:my_registrations')
