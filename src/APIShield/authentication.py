from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from keycloak import KeycloakOpenID
from django.conf import settings

class KeycloakOAuth2Authentication(BaseAuthentication):
    def authenticate(self, request):
        token = request.session.get('access_token')

        if not token:
            return None

        try:
            keycloak_openid = KeycloakOpenID(server_url=settings.KEYCLOAK_SERVER_URL,
                                             client_id=settings.KEYCLOAK_CLIENT_ID,
                                             realm_name=settings.KEYCLOAK_REALM_NAME,
                                             client_secret_key=settings.KEYCLOAK_CLIENT_SECRET)
           
            token_info = keycloak_openid.introspect(token)
            print('token_info: ', token_info)

            if not token_info['active']:
                raise AuthenticationFailed('Inactive User.')

            request.user = token_info
        except Exception as e:
            raise AuthenticationFailed(str(e))

        return (request.user, token)
