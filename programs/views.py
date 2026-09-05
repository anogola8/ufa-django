from django.shortcuts import render, get_object_or_404
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from django.shortcuts import redirect
from .models import Program
from .forms import ProgramForm

def program_list(request):
    # View all active programs
    programs = Program.objects.filter(is_active=True).order_by('order', 'title')
    featured_programs = programs.filter(is_featured=True)
    
    context = {
        'programs': programs,
        'featured_programs': featured_programs,
    }
    return render(request, 'programs/list.html', context)

def program_detail(request, slug):
    # View single program
    program = get_object_or_404(Program, slug=slug, is_active=True)
    context = {'program': program}
    return render(request, 'programs/detail.html', context)

@staff_member_required
def admin_programs(request):
    # Admin view for program management
    programs = Program.objects.all().order_by('order', 'title')
    context = {'programs': programs}
    return render(request, 'dashboard/admin_programs_management.html', context)

@staff_member_required
def admin_program_add(request):
    # Add a new program
    if request.method == 'POST':
        form = ProgramForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Program added successfully!')
            return redirect('programs:admin_list')
    else:
        form = ProgramForm()
    return render(request, 'dashboard/admin_program_form.html', {'form': form, 'title': 'Add Program'})

@staff_member_required
def admin_program_edit(request, program_id):
    # Edit a program
    program = get_object_or_404(Program, id=program_id)
    if request.method == 'POST':
        form = ProgramForm(request.POST, request.FILES, instance=program)
        if form.is_valid():
            form.save()
            messages.success(request, 'Program updated successfully!')
            return redirect('programs:admin_list')
    else:
        form = ProgramForm(instance=program)
    return render(request, 'dashboard/admin_program_form.html', {'form': form, 'title': 'Edit Program'})

@staff_member_required
def admin_program_delete(request, program_id):
    # Delete a program
    program = get_object_or_404(Program, id=program_id)
    if request.method == 'POST':
        program.delete()
        messages.success(request, 'Program deleted successfully!')
        return redirect('programs:admin_list')
    return render(request, 'dashboard/admin_confirm_delete.html', {'object': program, 'type': 'Program'})
