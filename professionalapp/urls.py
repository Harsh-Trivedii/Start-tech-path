from django.urls import path
from professionalapp import views

urlpatterns=[
    path('professional/home/',views.index_view_prof,name='homepage'),
    path('professional/addjob/',views.add_job_opening,name='addjob'),
    path('professional/viewapplicants/',views.view_applicants,name='viewapplicants'),
    path('professional/login/', views.professional_login_view, name='professional_login'),
    path('professional/signup/', views.signup_view, name='professional_signup'),
    path('professional/manageprofile/',views.manage_professional_profile,name='manageprofile'),
    path('logout/',views.logout_view, name='professional_logout_view'),
    path('approve/<int:applicant_id>/', views.approve_applicant, name='approve_applicant'),
]