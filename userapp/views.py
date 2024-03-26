from django.shortcuts import render,redirect,get_object_or_404
from userapp.forms import SignUpForm,UserProfileForm,SubscriptionForm
from django.contrib.auth import authenticate, login,logout
from userapp.forms import CustomAuthenticationForm,ContactForm
from django.http import HttpResponseRedirect,HttpResponse
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from userapp.models import Job,UserProfile,Subscription,PasswordReset
from datetime import datetime, timedelta
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib import messages
from professionalapp.models import JobApplicant,JobOpening
from userapp.utils import user_eligible
from django.utils.crypto import get_random_string
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.views import View
from django.conf import settings

# Create your views here.


# User Signup View
def signup_view(request):
    form = SignUpForm()
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(user.password)
            user.save()
            return redirect('login_view')  # Redirect to login_view after regular signup

    context = {'form': form}
    return render(request, 'registration/signup.html', context)


def login_view(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, request.POST)
        #import pdb;pdb.set_trace()
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            # Authenticate the user based on username and password
            user = authenticate(request=request, username=username, password=password)

            if user is not None:
                # For users
                login(request, user)
                return redirect(index_view)

            else:
                # Invalid login, handle accordingly
                form.add_error(None, 'Invalid login credentials')
    else:
        form = CustomAuthenticationForm(request)

    return render(request, 'registration/login.html', {'form': form})
    

def forgot_password(request):
    success_message=""
    fail_message=""
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        user = User.objects.filter(username=username, email=email).first()

        if user:
            # Generate a unique token
            token = get_random_string(length=32)

            # Save the token in the PasswordReset model
            reset = PasswordReset.objects.create(user=user, token=token)

            # Send an email with the reset link
            reset_link = f'{settings.BASE_URL}/reset-password/{token}/'
            send_mail('Password Reset', f'Click the following link to reset your password: {reset_link}', settings.EMAIL_HOST_USER, [email])

            success_message='Password reset link sent to your email. Please check your inbox.'
        else:
            fail_message='No such user (username or registered mail is incorrect)'

    return render(request, 'userapp/forgot_password.html',{'success_message':success_message,'fail_message':fail_message})




class ResetPasswordView(View):
    success_message=""
    def get(self, request, token):
        reset = PasswordReset.objects.filter(token=token, is_valid=True).first()

        if not reset:
            return HttpResponse('Invalid or expired token.')

        # Render the reset password form
        return render(request, 'userapp/reset_password.html', {'token': token})

    def post(self, request, token):
        reset = PasswordReset.objects.filter(token=token, is_valid=True).first()

        if not reset:
            return HttpResponse('Invalid or expired token.')

        password = request.POST.get('password')

        # Update the user's password
        reset.user.password = make_password(password)
        reset.user.save()

        # Mark the password reset token as used
        reset.is_valid = False
        reset.save()

        success_message = "Password reset successful. You can now login with your new password."

        return render(request, 'userapp/reset_password.html', {'token': token, 'success_message': success_message})



#To logout
def logout_view(request):
    logout(request)
    return redirect('login_view')

#MainPage View
@login_required(login_url='login_view')
def index_view(request):
    #print(request.user.is_authenticated)
    messages_con=""
    form=ContactForm()
    if request.method=='POST':
        form=ContactForm(request.POST)
        if form.is_valid():
            form.save()
            print('form is valid and feedback successfully saved in the database')

            subject='Thanks for filling the form.'
            message='This mail is from team START TECH PATH and is to inform you that your message is successfully received.'
            from_email='harshtrivedi1400@gmail.com'
            recipient_list=[form.cleaned_data['email']]
            send_mail(subject,message,from_email,recipient_list)
            messages_con="Your message is successfully received."
    form=ContactForm()
    context={
        'form':form,
        'messages':messages_con,
    }
    return render(request,'userapp/mainpage.html',context)

# views.py
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render
from .models import Job

# JobList View with pagination
def joblist_view(request):
    job_list = Job.objects.all()

    # Set the number of items per page
    items_per_page = 6
    joblist_paginator = Paginator(job_list, items_per_page)

    # Get the current page number from the request
    page = request.GET.get('page')

    try:
        joblist = joblist_paginator.page(page)
    except PageNotAnInteger:
        # If the page parameter is not an integer, set it to the first page
        joblist = joblist_paginator.page(1)
    except EmptyPage:
        # If the page is out of range, deliver the last page
        joblist = joblist_paginator.page(joblist_paginator.num_pages)

    context = {
        'joblist': joblist,
    }
    return render(request, 'userapp/joblist.html', context)




#User profile view
@login_required
def manage_profile(request):
    success_message=""
    try:
        user_profile = UserProfile.objects.get(user=request.user)
    except UserProfile.DoesNotExist:
        # If UserProfile does not exist, create a new one
        user_profile = UserProfile(user=request.user)
        user_profile.save()
   #print(user_profile.profile_photo.url)
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=user_profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile has been updated successfully!')
            success_message="Your profile has been updated successfully!"
    else:
        form = UserProfileForm(instance=user_profile)

    context = {'form': form, 'user_profile': user_profile, 'success_message':success_message}
    return render(request, 'userapp/profile.html', context)

@login_required
def subscription_view(request):
    existing_subscription = Subscription.objects.filter(user=request.user).first()
            
    if request.method == 'POST':
        form = SubscriptionForm(request.POST)
        if form.is_valid():
            # If no existing subscription, create a new one
            if existing_subscription:
                user_profile = get_object_or_404(UserProfile, user=request.user)
                user_profile.is_premium = existing_subscription.is_premium
                user_profile.save()
                return redirect('subscribe')
            subscription = form.save(commit=False)
            subscription.user = request.user
            subscription.is_premium = False
            subscription.payment_status = False
            subscription.subscription_expiry = datetime.now() + timedelta(days=365)
            subscription.save()

            messages.success(request, 'Subscription successful. Admin approval pending.')

            # Redirect to the payment details page
            return redirect('payment_details')  # Change 'payment_details' to your actual URL name
    else:
        form = SubscriptionForm()

    return render(request, 'userapp/subscription.html', {'form': form,'existing_subscription':existing_subscription,})

@login_required
def payment_details(request):
    success_message=""
    if request.method == 'POST':
        # Send an email to the user
        subject = 'Payment Confirmation'
        message = 'Thank you for your payment. Your subscription is pending approval and will be confirmed within 24 hours.'
        from_email = 'harshtrivedi1400@gmail.com'  # Replace with your email
        recipient_list = [request.user.email]
        success_message="Your payment will be approved by admin. Once approved you can view your profile as Premium in your manage profile."
        send_mail(subject, message, from_email, recipient_list, fail_silently=True)

    return render(request, 'userapp/payment_details.html',{'success_message':success_message,})


@login_required
def see_active_referrals(request):
    try:
        is_premium_user = request.user.userprofile.is_premium
    except UserProfile.DoesNotExist:
        is_premium_user = False

    success_message = ""
    applied_message = ""
    fail_message = ""

    success_job_id = -1
    applied_job_id = -1
    fail_job_id = -1
    if is_premium_user:
        active_referrals = JobOpening.objects.filter(is_active=True)

        if request.method == 'POST':
            job_id = request.POST.get('job_id')
            job = JobOpening.objects.get(id=job_id)
            
            # Check eligibility criteria and apply
            if user_eligible(request.user.userprofile, job):
                applicant, created = JobApplicant.objects.get_or_create(job=job, applicant=request.user.userprofile)
                if created:
                    success_message = "Your details are successfully submitted to the professional. You will receive update via email if your profile is approved by the professional. "
                    success_job_id = int(job_id)
                else:
                    applied_message = "You have already applied for this job."
                    applied_job_id = int(job_id)
            else:
                fail_message = "You do not meet the eligibility criteria for this job"
                fail_job_id = int(job_id)
        #import pdb;pdb.set_trace() 
        context = {
            'active_referrals': active_referrals,
            'success_message': success_message,
            'applied_message': applied_message,
            'fail_message': fail_message,
            'success_job_id': success_job_id,
            'applied_job_id': applied_job_id,
            'fail_job_id': fail_job_id,
        }
        return render(request, 'userapp/see_referrals.html', context)
