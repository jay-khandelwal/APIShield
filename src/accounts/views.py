

from django.shortcuts import redirect, render
from django.conf import settings
from django.http import HttpResponseBadRequest, HttpResponseServerError
from keycloak.exceptions import KeycloakAuthenticationError, KeycloakGetError
from keycloak import KeycloakOpenID

document_owner_scope = "list:self.documents retrieve:self.documents create:self.documents update:self.documents delete:self.documents"

def login_view(request):
    keycloak_openid = KeycloakOpenID(server_url=settings.KEYCLOAK_SERVER_URL,
                                     client_id=settings.KEYCLOAK_CLIENT_ID,
                                     realm_name=settings.KEYCLOAK_REALM_NAME,
                                     client_secret_key=settings.KEYCLOAK_CLIENT_SECRET)
    auth_url = keycloak_openid.auth_url(redirect_uri=settings.KEYCLOAK_REDIRECT_URI, scope="openid profile email "+document_owner_scope, state="your_state_info")
    return redirect(auth_url)


def callback_view(request):
    code = request.GET.get('code')
    if not code:
        return HttpResponseBadRequest("Missing authorization code")

    keycloak_openid = KeycloakOpenID(server_url=settings.KEYCLOAK_SERVER_URL,
                                     client_id=settings.KEYCLOAK_CLIENT_ID,
                                     realm_name=settings.KEYCLOAK_REALM_NAME,
                                     client_secret_key=settings.KEYCLOAK_CLIENT_SECRET)

    try:
        token = keycloak_openid.token(code=code, redirect_uri=settings.KEYCLOAK_REDIRECT_URI, grant_type='authorization_code')
        access_token = token['access_token']

        print("access_token: ", access_token)

        user_info = keycloak_openid.userinfo(access_token)
        user_id = user_info['sub']

        # Create a Django session
        request.session['access_token'] = access_token
        request.session['user_info'] = user_info
        request.session['user_id'] = user_id

        return redirect('/') 

    except KeycloakAuthenticationError as e:
        print(f'Authentication error: {e}')
        return HttpResponseServerError("Authentication failed")

    except KeycloakGetError as e:
        print(f'Error getting token or user info: {e}')
        return HttpResponseServerError("Failed to retrieve token or user info")


def home(request):
    if not request.session.get('access_token'):
        return redirect('accounts_login')

    user_info = request.session.get('user_info')
    return render(request, 'accounts/home.html', {'user_info': user_info})