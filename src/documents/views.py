from rest_framework import viewsets, status
from rest_framework.response import Response

from documents.permissions import HasScopePermission, HasRolePermission
from .models import Document
from .serializers import DocumentSerializer

class DocumentAdminViewSet(viewsets.ModelViewSet):
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer
    default_permission_classes = [HasRolePermission(), ]

    permission_classes = {
        "list": [HasRolePermission(['documents.read', ]), ],
        "retrieve": [HasRolePermission(['documents.read', ]), ],
        "create": [HasRolePermission(['documents.write', ]), ],
        "put": [HasRolePermission(['documents.write', ]), ],
        "delete": [HasRolePermission(['documents.delete', ]), ],
    }

    def get_serializer_context(self):
        context =  super().get_serializer_context()
        context['user_id'] = self.request.session.get('user_id')
        return context

    def get_permissions(self):
        permission_classes = self.permission_classes.get(
            self.action, self.default_permission_classes)
        return [permission for permission in permission_classes]
    
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)
    

class DocumentOwnerViewSet(viewsets.ModelViewSet):
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer
    default_permission_classes = [HasScopePermission(), ]

    permission_classes = {
        "list": [HasScopePermission(['list:self.documents', ]), ],
        "retrieve": [HasScopePermission(["retrieve:self.documents", ]), ],
        "create": [HasScopePermission(["create:self.documents", ]), ],
        "put": [HasScopePermission(["update:self.documents", ]), ],
        "delete": [HasScopePermission(["delete:self.documents", ]), ],
    }

    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.filter(owner=self.request.session['user_id'])
        return qs
    

    def get_serializer_context(self):
        context =  super().get_serializer_context()
        context['user_id'] = self.request.session.get('user_id')
        return context

    def get_permissions(self):
        permission_classes = self.permission_classes.get(
            self.action, self.default_permission_classes)
        return [permission for permission in permission_classes]

    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)