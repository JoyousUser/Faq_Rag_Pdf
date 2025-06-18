from django.urls import path
from .views import LoginView, UserViewSet, LogoutView

urlpatterns = [
    path('users/', UserViewSet.as_view({'get': 'list'})),
    path('login/', LoginView.as_view()),
    path('logout/', LogoutView.as_view())
]