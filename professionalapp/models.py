from django.db import models
from userapp.models import UserProfile
# Create your models here.

# Professional user login and signup model
class ProfessionalUser(models.Model):
    username = models.CharField(max_length=150, unique=True)
    password = models.CharField(max_length=128)
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    is_professional = models.BooleanField(default=True)

    def __str__(self):
        return self.username


#Professional user Job post model
class JobOpening(models.Model):
    EXPERIENCE_CHOICES = [
        ('Fresher', 'Fresher'),
        ('<1 year', '<1 year'),
        ('>1 year', '>1 year'),
    ]

    GRADE_CHOICES = [
        ('>60%', 'Above 60%'),
        ('>70%', 'Above 70%'),
        ('>80%', 'Above 80%'),
    ]

    company_name = models.CharField(max_length=100)
    job_id = models.CharField(max_length=50, unique=True)
    eligibility_criteria = models.TextField()
    job_position = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    experience = models.CharField(max_length=20, choices=EXPERIENCE_CHOICES, blank=True, null=True)
    passing_year = models.PositiveIntegerField(blank=True, null=True)
    grade = models.CharField(max_length=20, choices=GRADE_CHOICES, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    referral_link = models.URLField(blank=True, null=True)
    def __str__(self):
        return f"{self.company_name} - {self.job_position}"

    def applicants(self):
        return JobApplicant.objects.filter(job=self)



# Job Applicant Data model
class JobApplicant(models.Model):
    job = models.ForeignKey(JobOpening, on_delete=models.CASCADE)
    applicant = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    application_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.applicant.user.username} - {self.job.company_name} - {self.job.job_position}'
    


class ProfessionalProfile(models.Model):
    user = models.OneToOneField('ProfessionalUser', on_delete=models.CASCADE)
    contact_number = models.CharField(max_length=15)
    city = models.CharField(max_length=100)
    company_name = models.CharField(max_length=100)
    job_position = models.CharField(max_length=100)
    document = models.FileField(upload_to='documents/')
    profile_photo = models.ImageField(upload_to='profile_photos/', blank=True, null=True)
    is_approved = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username}'s Profile"