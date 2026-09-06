from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from members.models import Member
from core.models import County, Ward
from core.leadership_positions import ALL_POSITIONS

class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'class': 'form-control'}))
    first_name = forms.CharField(max_length=30, required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(max_length=30, required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    phone_number = forms.CharField(max_length=15, required=True, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., 0712345678'}))
    
    # County dropdown
    county = forms.ModelChoiceField(
        queryset=County.objects.all().order_by('name'),
        required=True,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    ward = forms.ModelChoiceField(
        queryset=Ward.objects.all().order_by('name'),
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    # Leadership position - using ALL_POSITIONS
    leadership_position = forms.ChoiceField(
        choices=[('', 'Select Leadership Position')] + ALL_POSITIONS,
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['county'].empty_label = "Select your County"
        self.fields['ward'].empty_label = "Select your Ward (optional)"
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('This email is already registered.')
        return email
    
    def clean_phone_number(self):
        phone = self.cleaned_data.get('phone_number')
        if Member.objects.filter(phone_number=phone).exists():
            raise forms.ValidationError('This phone number is already registered.')
        return phone
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        
        if commit:
            user.save()
            # Create Member profile
            Member.objects.create(
                user=user,
                full_name=f"{user.first_name} {user.last_name}",
                email=user.email,
                phone_number=self.cleaned_data['phone_number'],
                county=self.cleaned_data['county'],
                ward=self.cleaned_data.get('ward'),
                membership_status='pending',
                membership_type='youth',
                leadership_position=self.cleaned_data.get('leadership_position'),
            )
            
        return user

class ProfileForm(forms.ModelForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}))
    first_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
        }

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Member
        fields = ['phone_number', 'date_of_birth', 'gender', 'county', 'ward', 'address', 'city', 'bio', 'leadership_position']
        widgets = {
            'phone_number': forms.TextInput(attrs={'class': 'form-control'}),
            'date_of_birth': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'gender': forms.Select(attrs={'class': 'form-control'}),
            'county': forms.Select(attrs={'class': 'form-control'}),
            'ward': forms.Select(attrs={'class': 'form-control'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'city': forms.TextInput(attrs={'class': 'form-control'}),
            'bio': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'leadership_position': forms.Select(attrs={'class': 'form-control'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['county'].empty_label = "Select County"
        self.fields['ward'].empty_label = "Select Ward"
        self.fields['leadership_position'].choices = [('', 'Select Leadership Position')] + ALL_POSITIONS

# Backward compatibility
UserUpdateForm = ProfileForm
