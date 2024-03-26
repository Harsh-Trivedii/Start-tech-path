from django.contrib import admin
from userapp.models import Job,Contact,UserProfile,Subscription
# Register your models here.

#Contact model Admin
class ContactAdmin(admin.ModelAdmin):
    list_display=['name','email','message']
admin.site.register(Contact,ContactAdmin)

#Job model Admin
class JobAdmin(admin.ModelAdmin):
    list_display=['company_name','position','salary','location','job_type']
admin.site.register(Job,JobAdmin)



#User profile model Admin
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'contact_number', 'address', 'institute', 'year', 'grade', 'degree', 'branch', 'experience', 'skills', 'resume', 'profile_photo')
admin.site.register(UserProfile, UserProfileAdmin)


#User membership subscription
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('user', 'is_premium', 'payment_status', 'subscription_expiry')
admin.site.register(Subscription, SubscriptionAdmin)
