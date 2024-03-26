from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from userapp.models import Contact,UserProfile,Subscription


#User Signup Form
class SignUpForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model=User
        fields=['username','password','email','first_name','last_name']


#User Login Form (using django inbuilt AuthenticationForm)
class CustomAuthenticationForm(AuthenticationForm):
    pass

#contact form
class ContactForm(forms.ModelForm):
    message=forms.CharField(widget=forms.Textarea(attrs={'rows':4}))
    class Meta:
        model=Contact
        fields='__all__'


#User Profile form
class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['contact_number', 'address', 'institute', 'year', 'grade', 'degree', 'branch', 'experience', 'skills', 'resume', 'profile_photo']

        def clean_resume(self):
          resume = self.cleaned_data['resume']
          if resume:
            if not resume.name.endswith('.pdf'):
                raise forms.ValidationError('Only PDF files are allowed.')
          return resume
        

#Membership Subscription Form
class SubscriptionForm(forms.ModelForm):
    class Meta:
        model = Subscription
        fields = []