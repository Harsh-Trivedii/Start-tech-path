from django.shortcuts import redirect
from functools import wraps
from django.http import HttpResponseForbidden
from professionalapp.models import ProfessionalUser

def professional_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        # Check if professional user is logged in
        if 'professional_id' in request.session and request.session.get('is_professional', False):
            professional_id = request.session['professional_id']
            try:
                professional = ProfessionalUser.objects.get(id=professional_id)
                # You can perform additional checks here if needed
                return view_func(request, *args, **kwargs)
            except ProfessionalUser.DoesNotExist:
                # Handle the case where the professional user doesn't exist
                return redirect('professional_login')  # Redirect to login page
        # If not logged in as professional, return forbidden response
        return HttpResponseForbidden("You do not have permission to access this page.")
    return _wrapped_view