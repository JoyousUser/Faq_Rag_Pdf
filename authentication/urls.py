from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from authentication.views.ProtectedView_test import ProtectedView
from authentication.views.LoginView import GoogleJWTAPIView
from authentication.views.LogoutView import GoogleLogoutView
from authentication.views.UserInfoView import UserInfoView

urlpatterns = [
    path('token/google/', GoogleJWTAPIView.as_view(), name='token_google'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('logout/', GoogleLogoutView.as_view(), name='logout'),
    path('protected/', ProtectedView.as_view(), name='protected'),
    path("user/", UserInfoView.as_view(), name="user_info"),
]
