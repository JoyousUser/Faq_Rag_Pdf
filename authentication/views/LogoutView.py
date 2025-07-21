from django.contrib.auth import logout
from django.http import JsonResponse
from rest_framework import permissions
from rest_framework.views import APIView

from faq_project import settings


class GoogleLogoutView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        response = JsonResponse({"message": "Logged out successfully"})
        response.delete_cookie("csrftoken")
        response.delete_cookie(
            settings.SIMPLE_JWT.get('AUTH_COOKIE'),
            path=settings.SIMPLE_JWT.get('AUTH_COOKIE_PATH', '/'),
            domain=settings.SIMPLE_JWT.get('AUTH_COOKIE_DOMAIN', None),
            samesite=settings.SIMPLE_JWT.get('AUTH_COOKIE_SAMESITE', 'Lax'),
        )
        response.delete_cookie('sessionid')
        response.delete_cookie('refresh_token')


        return response