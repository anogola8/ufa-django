from django import forms
from .models import Appointment
from members.models import Member
from core.models import County, Ward
from core.leadership_positions import ALL_POSITIONS

class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['member', 'position', 'county', 'ward', 'effective_date', 'expiry_date', 'notes']
        widgets = {
            'member': forms.Select(attrs={'class': 'form-control'}),
            'position': forms.Select(attrs={'class': 'form-control'}),
            'county': forms.Select(attrs={'class': 'form-control'}),
            'ward': forms.Select(attrs={'class': 'form-control'}),
            'effective_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'expiry_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Only show active members
        self.fields['member'].queryset = Member.objects.filter(membership_status='active')
        self.fields['position'].choices = [('', 'Select Position')] + ALL_POSITIONS
        self.fields['county'].empty_label = "Select County"
        self.fields['ward'].empty_label = "Select Ward"
        self.fields['county'].queryset = County.objects.all().order_by('name')
        
        # Only load wards if county is selected
        if self.instance and self.instance.pk and self.instance.county:
            self.fields['ward'].queryset = Ward.objects.filter(county=self.instance.county).order_by('name')
        else:
            self.fields['ward'].queryset = Ward.objects.none()
