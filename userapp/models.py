from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
# Create your models here.



# Password Reset Model
class PasswordReset(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    token = models.CharField(max_length=100, unique=True)
    created_at = models.DateTimeField(default=timezone.now)
    is_valid = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.user.username} - {self.created_at}'


#Contact details model
class Contact(models.Model):
    name=models.CharField(max_length=30)
    email=models.EmailField(max_length=40)
    message=models.CharField(max_length=300)


#Job details model
class Job(models.Model):
    company_name=models.CharField(max_length=40)
    position=models.CharField(max_length=40)
    salary=models.CharField(max_length=20)
    location=models.CharField(max_length=30)
    job_type=models.CharField(max_length=30)
    company_website = models.URLField()

    def __str__(self):
        return self.company_name
    
#User Profile model
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    contact_number = models.CharField(max_length=10, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    institute = models.CharField(max_length=100, blank=True, null=True)
    year = models.PositiveIntegerField(blank=True, null=True)
    grade = models.CharField(max_length=10, blank=True, null=True)
    degree = models.CharField(max_length=50, blank=True, null=True)
    branch = models.CharField(max_length=50, blank=True, null=True)
    experience = models.CharField(max_length=20, choices=[('Fresher', 'Fresher'), ('<1 year', '<1 year'), ('>1 year', '>1 year')], blank=True, null=True)
    skills = models.TextField(blank=True, null=True)
    resume = models.FileField(upload_to='resumes/', blank=True, null=True)
    profile_photo = models.ImageField(upload_to='profile_photos/', blank=True, null=True)
    is_premium = models.BooleanField(default=False)

    def subscription_status(self):
        if self.is_premium:
            return "Premium"
        else:
            return "Normal"
        
    def __str__(self):
        return f'{self.user.username} Profile'  
    

# Membership Subscription
class Subscription(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_premium = models.BooleanField(default=False)
    payment_status = models.BooleanField(default=False)
    subscription_expiry = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f'{self.user.username} Subscription'

    def save(self, *args, **kwargs):
        # Call the parent class's save method
        super().save(*args, **kwargs)

        # Update the corresponding UserProfile
        user_profile = UserProfile.objects.get(user=self.user)
        user_profile.is_premium = self.is_premium
        user_profile.save()

