from rest_framework.permissions import BasePermission

class HasScopePermission(BasePermission):

    def __init__(self, required_scopes=None):
        self.required_scopes = required_scopes

    def has_permission(self, request, view):
        if self.required_scopes is None:
            return False
        user = request.user
        token_scopes = user.get('scope', '').split()
        return any(scope in token_scopes for scope in self.required_scopes)
    

class HasRolePermission(BasePermission):

    def __init__(self, required_roles=None):
        self.required_roles = required_roles

    def has_permission(self, request, view):
        if self.required_roles is None:
            return False
        
        user = request.user
        realm_access = user.get('realm_access', {})
        roles = realm_access.get('roles', [])

        return any(role in roles for role in self.required_roles)