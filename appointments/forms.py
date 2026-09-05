from django import forms
from .models import Appointment
from members.models import Member

class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['member', 'position', 'county', 'ward', 'effective_date', 'expiry_date', 'notes']
        widgets = {
            'member': forms.Select(attrs={'class': 'form-control'}),
            'position': forms.Select(attrs={'class': 'form-control'}),
            'county': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., Kakamega'}),
            'ward': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., Lurambi'}),
            'effective_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'expiry_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Only show active members
        self.fields['member'].queryset = Member.objects.filter(membership_status='active')
