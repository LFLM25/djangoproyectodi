# middleware.py

from django.shortcuts import redirect
from django.urls import reverse

class AuthRequiredMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Verifica si el usuario está intentando acceder a la página de inicio
        if request.path == reverse('inicio') and not request.user.is_authenticated:
            return redirect('login')  # Redirige a la página de login
        response = self.get_response(request)
        return response
