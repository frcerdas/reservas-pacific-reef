from django.shortcuts import redirect
from django.urls import reverse
from django.contrib.auth.models import AnonymousUser

class LoginRequiredMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if not isinstance(request.user, AnonymousUser) and not request.user.is_authenticated and not request.path == reverse('login'):
            return redirect(reverse('login'))
        
        response = self.get_response(request)
        return response
