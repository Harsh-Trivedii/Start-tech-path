from django.shortcuts import render,redirect
from professionalapp.models import JobOpening,ProfessionalUser,ProfessionalProfile,JobApplicant
from professionalapp.forms import JobOpeningForm,ProfessionalSignUpForm,ProfessionalProfileForm
from userapp.forms import ContactForm
from django.core.mail import send_mail
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.hashers import check_password
from professionalapp.decorators import professional_required
from django.shortcuts import get_object_or_404
from django.contrib import messages
from django.http import HttpResponseNotFound,HttpResponseRedirect
from django.urls import reverse
# Create your views here.

def signup_view(request):
    if request.method == 'POST':
        form = ProfessionalSignUpForm(request.POST)
        if form.is_valid():
            professional = form.save(commit=False)
            professional.password = make_password(form.cleaned_data['password'])  # Hash the password
            professional.save()
            return redirect(professional_login_view)  # Redirect to the login page after successful signup
    else:
        form = ProfessionalSignUpForm()
    return render(request, 'professionalapp/signup.html', {'form': form})

def professional_login_view(request):
    error_message = ''
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        try:
            professional = ProfessionalUser.objects.get(username=username)
            if check_password(password, professional.password) and professional.is_professional:
                # Login successful, set session variables
                request.session['professional_id'] = professional.id
                request.session['is_professional'] = True
                # Redirect to the index page after successful login
                return redirect(index_view_prof)
            else:
                error_message = 'Invalid username or password.'
        except ProfessionalUser.DoesNotExist:
            error_message = 'User does not exist.'
    return render(request, 'professionalapp/login.html', {'error_message': error_message})



#To logout
def logout_view(request):
    logout(request)
    return redirect(professional_login_view)


#Mainpage view
@professional_required
def index_view_prof(request):
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
    return render(request,'professionalapp/index.html',context)

@professional_required
def add_job_opening(request):
    error_message=""
    success_message = ""
    if request.method == 'POST':
        form = JobOpeningForm(request.POST)
        professional_id = request.session.get('professional_id')
        try:
            professional_profile = ProfessionalProfile.objects.get(user_id=professional_id)
        except ProfessionalProfile.DoesNotExist:
            professional_profile = None

        if professional_profile and not professional_profile.is_approved:
            error_message = "Your profile is pending approval from admin. Only admin-approved profiles are allowed to add jobs. You can view approval status in your profile."
        else:  
            if form.is_valid():
                company_name = form.cleaned_data.get('company_name')
                
                # Check if the entered company name matches the company name stored in professional profile
                if professional_profile and company_name == professional_profile.company_name:
                    form.save()
                    success_message = "Job Opening added successfully, now users will be able to view and apply for the job."
                else:
                    error_message = "The entered company name does not match your registered company name."
                    success_message=""
            else:
                error_message = "There was an error adding the job opening. Please check the form."
    else:
        form = JobOpeningForm()
        success_message = ""
        error_message = ""
    return render(request, 'professionalapp/job_opening.html', {'form': form, 'success_message': success_message, 'error_message': error_message})

@professional_required
def view_applicants(request):
    try:
        # Retrieve the professional's profile
        professional_id = request.session.get('professional_id')
        professional_profile, created = ProfessionalProfile.objects.get_or_create(user_id=professional_id)
        # Fetch all applicants for the jobs posted by the professional
        applicants = JobApplicant.objects.filter(job__company_name=professional_profile.company_name)
    except ProfessionalProfile.DoesNotExist:
        # Handle the case where the professional profile doesn't exist
        return HttpResponseNotFound("Professional profile not found")

    # Extract UserProfile objects for each applicant
    applicant_profiles = [applicant.applicant.user.userprofile for applicant in applicants]
    success_message = request.session.pop('success_message', None)
    return render(request, 'professionalapp/view_applicants.html', {'applicants': zip(applicants, applicant_profiles),'professional_profile': professional_profile,'success_message': success_message})

@professional_required
def approve_applicant(request, applicant_id):
    try:
        # Get the professional user ID from the session
        professional_id = request.session.get('professional_id')

        # Retrieve the professional profile using the ID
        professional_profile, created = ProfessionalProfile.objects.get_or_create(user_id=professional_id)

        # Fetch the applicant and related details
        applicant = JobApplicant.objects.get(id=applicant_id)
        applicant_profile = applicant.applicant
        job = applicant.job

        # Send email to the applicant
        subject = f"Your Application for {job.company_name} - {job.job_position} is Approved"
        message = f"Dear {applicant_profile.user.first_name},\n\nCongratulations! Your application for the position at {job.company_name} - {job.job_position} has been approved. Please find the referral link below:\n\n{job.referral_link} (Referral email: {professional_profile.user.email})\n\nYou can apply using the referral link provided above.\n\nRegards,\n{professional_profile.user.first_name} {professional_profile.user.last_name}"
        recipient_list = [applicant_profile.user.email]
        send_mail(subject, message, professional_profile.user.email, recipient_list)


        # Add success message
        success_message = f"Email with referral link has been sent to {applicant_profile.user.username}"
        request.session['success_message'] = success_message
        return HttpResponseRedirect(reverse('viewapplicants'))

    except JobApplicant.DoesNotExist:
        return HttpResponseNotFound("Applicant not found")


# def manage_professional_profile(request):
#     success_message=""
#     try:
#         profile = request.user.professionalprofile
#     except ProfessionalProfile.DoesNotExist:
#         profile = None

#     if request.method == 'POST':
#         form = ProfessionalProfileForm(request.POST, request.FILES, instance=profile)
#         if form.is_valid():
#             profile = form.save(commit=False)
#             profile.user = request.user
#             profile.save()
#             success_message="Your profile has been updated successfully!"
#     else:
#         form = ProfessionalProfileForm(instance=profile)

#     return render(request, 'professionalapp/manageprofile.html', {'form': form,'success_message':success_message})


@professional_required
def manage_professional_profile(request):
    success_message = ""
    error_message = ""

    # Retrieve the professional user object using the session
    professional_id = request.session.get('professional_id')
    professional_user = ProfessionalUser.objects.first()
    
    # Attempt to retrieve the professional profile
    professional_profile, created = ProfessionalProfile.objects.get_or_create(user_id=professional_id)

    if request.method == 'POST':
        form = ProfessionalProfileForm(request.POST, request.FILES, instance=professional_profile)
        if form.is_valid():
            form.save()
            success_message = "Your profile has been updated successfully!"
        else:
            error_message = "There was an error updating your profile. Please check the form."
    else:
        # Ensure professional_profile is an instance of ProfessionalProfile
        if not isinstance(professional_profile, ProfessionalProfile):
            professional_profile = None
        form = ProfessionalProfileForm(instance=professional_profile)


    context = {
        'form': form,
        'professional_profile': professional_profile,
        'success_message': success_message,
        'error_message': error_message
    }
    return render(request, 'professionalapp/manageprofile.html', context)