from django.urls import path, include
from .views import LoginView, UserViewSet, LogoutView, FaqViewSet, UploadedFilesViewSet
from rest_framework import routers
from rest_framework_simplejwt.views import (TokenObtainPairView, TokenRefreshView,)

router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'faqs', FaqViewSet)
router.register(r'uploadedfiles', UploadedFilesViewSet)


urlpatterns = [
    path('login/', LoginView.as_view()),
    path('logout/', LogoutView.as_view()),
    path('', include(router.urls)),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]