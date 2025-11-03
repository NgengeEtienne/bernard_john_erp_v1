# user/middleware.py
from django.shortcuts import redirect
from django.urls import reverse
from django.utils.deprecation import MiddlewareMixin

class LoginRequiredMiddleware(MiddlewareMixin):
    def process_view(self, request, view_func, view_args, view_kwargs):
        excluded_paths = [
            reverse('login'),
            reverse('register'),
            reverse('forgot_password'),
            reverse('home'),
            '/admin/',  # Ensure admin site is excluded
        ]

        if not request.user.is_authenticated and request.path not in excluded_paths:
            return redirect('login')
        return None

# myapp/middleware.py

from django.utils import timezone
from django.conf import settings
from django.contrib.auth import logout

class AutoLogoutMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            last_activity = request.session.get('last_activity')
            if last_activity and (timezone.now() - last_activity > settings.SESSION_COOKIE_AGE):
                logout(request)
            request.session['last_activity'] = timezone.now()

        response = self.get_response(request)
        return response
