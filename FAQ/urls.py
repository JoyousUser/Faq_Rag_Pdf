from django.urls import path, include
from rest_framework import routers
from rest_framework_simplejwt.views import (TokenObtainPairView, TokenRefreshView,)

from .views import FaqViewSet, UploadedFilesViewSet
from .views.ProtectedView_test import ProtectedView
from .views.auth import GoogleJWTAPIView
from .views.logout_views import GoogleLogoutView

router = routers.DefaultRouter()
router.register(r'faqs', FaqViewSet)
router.register(r'uploadedfiles', UploadedFilesViewSet)


urlpatterns = [
    path('', include(router.urls)),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/google/', GoogleJWTAPIView.as_view(), name='token_google'),
    path('auth/logout/', GoogleLogoutView.as_view(), name='logout'),
    path('protected/', ProtectedView.as_view(), name='protected'),
]