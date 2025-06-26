from django.urls import path, include
from .views import FaqViewSet, UploadedFilesViewSet
from rest_framework import routers
from rest_framework_simplejwt.views import (TokenObtainPairView, TokenRefreshView,)

from .views.auth import GoogleJWTAPIView

router = routers.DefaultRouter()
router.register(r'faqs', FaqViewSet)
router.register(r'uploadedfiles', UploadedFilesViewSet)


urlpatterns = [
    path('', include(router.urls)),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/google/', GoogleJWTAPIView.as_view(), name='token_google'),
]