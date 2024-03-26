from django.urls import path,include
from userapp import views

urlpatterns=[
    path('signup/',views.signup_view,name='signup'),
    path('logout/',views.logout_view, name='logout_view'),
    path('',views.index_view,name='home'),
    path('login/',views.login_view,name='login_view'),
    path('jobs/',views.joblist_view,name='joblist'),
    path('manageprofile/',views.manage_profile,name='manage_profile'),
    path('subscribe/', views.subscription_view, name='subscribe'),
    path('payment-details/', views.payment_details, name='payment_details'),
    path('referrals/',views.see_active_referrals,name="see_active_referrals"),
    path('forgot-password/', views.forgot_password, name='forgot_password'),
    path('reset-password/<str:token>/', views.ResetPasswordView.as_view(), name='reset_password'),
]

