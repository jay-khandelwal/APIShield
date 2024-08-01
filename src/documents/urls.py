
from .views import DocumentAdminViewSet, DocumentOwnerViewSet

from rest_framework.routers import DefaultRouter

router = DefaultRouter()

router.register('admin', DocumentAdminViewSet, basename='DocumentAdminViewSet')
router.register('owner', DocumentOwnerViewSet, basename='DocumentOwnerViewSet')

urlpatterns = router.urls + []
