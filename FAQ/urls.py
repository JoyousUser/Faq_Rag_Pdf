from django.urls import path, include
from .views import LoginView, UserViewSet, LogoutView, FaqViewSet, UploadedFilesViewSet
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'faqs', FaqViewSet)
router.register(r'uploadedfiles', UploadedFilesViewSet)


urlpatterns = [
    path('login/', LoginView.as_view()),
    path('logout/', LogoutView.as_view()),
    # path('users/', UserViewSet.as_view({'get': 'list'})),
    # path('faqs/', FaqViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('', include(router.urls)),
]