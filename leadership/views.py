from django.shortcuts import render, get_object_or_404
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from django.shortcuts import redirect
from django.template.response import TemplateResponse
from .models import Leader
from .forms import LeaderForm

def leadership_list(request):
    """View all active leaders"""
    
    # Get NEC members (National Executive Council)
    nec_members = Leader.objects.filter(
        leader_type='nec', 
        is_active=True
    ).order_by('order')
    
    context = {
        'nec_members': nec_members,
    }
    
    # Force using the new template
    return TemplateResponse(request, 'leadership/list.html', context)

def leader_detail(request, slug):
    """View single leader"""
    leader = get_object_or_404(Leader, slug=slug, is_active=True)
    context = {'leader': leader}
    return TemplateResponse(request, 'leadership/detail.html', context)

# Admin Views for Leadership Management
@staff_member_required
def admin_leadership(request):
    """Admin view for leadership management"""
    leaders = Leader.objects.all().order_by('leader_type', 'order', '-created_at')
    context = {'leaders': leaders}
    return render(request, 'dashboard/admin_leadership.html', context)

@staff_member_required
def admin_leader_add(request):
    """Add a new leader"""
    if request.method == 'POST':
        form = LeaderForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Leader added successfully!')
            return redirect('admin_dashboard:leadership')
    else:
        form = LeaderForm()
    return render(request, 'dashboard/admin_leader_form.html', {'form': form, 'title': 'Add Leader'})

@staff_member_required
def admin_leader_edit(request, leader_id):
    """Edit a leader"""
    leader = get_object_or_404(Leader, id=leader_id)
    if request.method == 'POST':
        form = LeaderForm(request.POST, request.FILES, instance=leader)
        if form.is_valid():
            form.save()
            messages.success(request, 'Leader updated successfully!')
            return redirect('admin_dashboard:leadership')
    else:
        form = LeaderForm(instance=leader)
    return render(request, 'dashboard/admin_leader_form.html', {'form': form, 'title': 'Edit Leader'})

@staff_member_required
def admin_leader_delete(request, leader_id):
    """Delete a leader"""
    leader = get_object_or_404(Leader, id=leader_id)
    if request.method == 'POST':
        leader.delete()
        messages.success(request, 'Leader deleted successfully!')
        return redirect('admin_dashboard:leadership')
    return render(request, 'dashboard/admin_confirm_delete.html', {'object': leader, 'type': 'Leader'})
