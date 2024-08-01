from django.shortcuts import redirect
from django.conf import settings
from django.urls import reverse

class KeycloakAuthenticationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if not request.session.get('access_token') and not request.path==reverse('accounts_login') and request.path != reverse('accounts_callback') :
            return redirect('accounts_login')
        response = self.get_response(request)
        return response
