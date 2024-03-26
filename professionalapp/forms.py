from django import forms
from professionalapp.models import JobOpening,ProfessionalUser,ProfessionalProfile


class ProfessionalSignUpForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = ProfessionalUser
        fields = ['username', 'password', 'email', 'first_name', 'last_name']


class JobOpeningForm(forms.ModelForm):
    class Meta:
        model = JobOpening
        fields = ['company_name', 'job_id', 'eligibility_criteria', 'job_position', 'city', 'experience', 'passing_year', 'grade','referral_link']


class ProfessionalProfileForm(forms.ModelForm):
    class Meta:
        model = ProfessionalProfile
        fields = ['contact_number', 'city', 'company_name', 'job_position', 'document','profile_photo']
        labels = {
            'contact_number': 'Contact Number',
            'city': 'City',
            'company_name': 'Company Name',
            'job_position': 'Job Position',
            'document': 'Upload proof Document (PDF only, recent salary script or joining letter)',
            'profile_photo': 'Upload Photo (Jpeg/jpg/png only)',
        }