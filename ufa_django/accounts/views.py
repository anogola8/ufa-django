from django.contrib import messages
from django.contrib.auth import login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect, render

from core.models import AuditLog
from core.services import log_action

from .forms import ProfileForm, RegisterForm


def _client_ip(request):
    forwarded = request.META.get('HTTP_X_FORWARDED_FOR')
    if forwarded:
        return forwarded.split(',')[0].strip()
    return request.META.get('REMOTE_ADDR')


def register(request):
    if request.user.is_authenticated:
        return redirect('accounts:profile')

    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            log_action(
                actor=user, action=AuditLog.Action.CREATE, target=user,
                ip_address=_client_ip(request), object_repr=f'Account created: {user.email}',
            )
            messages.success(request, 'Welcome to UFA! Your account has been created.')
            return redirect('accounts:profile')
    else:
        form = RegisterForm()

    return render(request, 'accounts/register.html', {'form': form})


class EmailLoginView(LoginView):
    template_name = 'accounts/login.html'

    def form_valid(self, form):
        response = super().form_valid(form)
        log_action(
            actor=self.request.user, action=AuditLog.Action.LOGIN, target=self.request.user,
            ip_address=_client_ip(self.request),
        )
        return response


@login_required
def logout_view(request):
    log_action(
        actor=request.user, action=AuditLog.Action.LOGOUT, target=request.user,
        ip_address=_client_ip(request),
    )
    auth_logout(request)
    messages.info(request, "You've been logged out.")
    return redirect('core:home')


@login_required
def profile(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            log_action(
                actor=request.user, action=AuditLog.Action.UPDATE, target=request.user,
                ip_address=_client_ip(request), object_repr='Profile updated',
            )
            messages.success(request, 'Profile updated.')
            return redirect('accounts:profile')
    else:
        form = ProfileForm(instance=request.user)

    return render(request, 'accounts/profile.html', {'form': form})
