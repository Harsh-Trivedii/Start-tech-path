from django.contrib import admin
from professionalapp.models import JobOpening,JobApplicant,ProfessionalUser,ProfessionalProfile
# Register your models here.

class JobOpeningAdmin(admin.ModelAdmin):
    list_display = ('company_name', 'job_id', 'eligibility_criteria', 'job_position', 'city')
admin.site.register(JobOpening, JobOpeningAdmin)

class JobApplicantAdmin(admin.ModelAdmin):
    list_display = ('applicant_username', 'job_details', 'application_date')

    def applicant_username(self, obj):
        return obj.applicant.user.username
    applicant_username.short_description = 'Applicant Username'

    def job_details(self, obj):
        return f'{obj.job.company_name} - {obj.job.job_position}'
    job_details.short_description = 'Job Details'

admin.site.register(JobApplicant, JobApplicantAdmin)



class ProfessionalUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_professional')
admin.site.register(ProfessionalUser, ProfessionalUserAdmin)


class ProfessionalProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'contact_number', 'city', 'company_name', 'job_position', 'is_approved')
admin.site.register(ProfessionalProfile, ProfessionalProfileAdmin)