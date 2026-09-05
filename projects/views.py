from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from django.shortcuts import redirect
from .models import Project

def project_list(request):
    """View all projects"""
    projects = Project.objects.filter(status__in=['planning', 'ongoing']).order_by('-created_at')
    completed_projects = Project.objects.filter(status='completed').order_by('-end_date')
    
    context = {
        'projects': projects,
        'completed_projects': completed_projects,
    }
    return render(request, 'projects/list.html', context)

def project_detail(request, slug):
    """View single project"""
    project = get_object_or_404(Project, slug=slug)
    updates = project.updates.all()[:10] if hasattr(project, 'updates') else []
    
    context = {
        'project': project,
        'updates': updates,
    }
    return render(request, 'projects/detail.html', context)

@staff_member_required
def project_create(request):
    """Create a new project (staff only)"""
    if request.method == 'POST':
        messages.success(request, 'Project created successfully!')
        return redirect('projects:list')
    return render(request, 'projects/create.html')

@staff_member_required
def project_edit(request, slug):
    """Edit a project (staff only)"""
    project = get_object_or_404(Project, slug=slug)
    if request.method == 'POST':
        messages.success(request, 'Project updated successfully!')
        return redirect('projects:detail', slug=project.slug)
    return render(request, 'projects/edit.html', {'project': project})

@staff_member_required
def project_delete(request, slug):
    """Delete a project (staff only)"""
    project = get_object_or_404(Project, slug=slug)
    if request.method == 'POST':
        project.delete()
        messages.success(request, 'Project deleted successfully!')
        return redirect('projects:list')
    return render(request, 'projects/delete.html', {'project': project})
