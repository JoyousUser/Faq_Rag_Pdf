from django.urls import path, include
from rest_framework import routers

from .views import FaqViewSet, UploadedFilesViewSet

router = routers.DefaultRouter()
router.register(r'faqs', FaqViewSet)
router.register(r'uploadedfiles', UploadedFilesViewSet)


urlpatterns = [
    path('', include(router.urls)),
]