from django.contrib.auth import logout
from django.http import JsonResponse
from rest_framework import permissions
from rest_framework.views import APIView

from faq_project import settings


class GoogleLogoutView(APIView):
    permission_classes = [permissions.AllowAny]

    def options(self, request, *args, **kwargs):
        response = JsonResponse({});
        response["Access-Control-Allow-Origin"] = "http://localhost:5173"
        response["Access-Control-Allow-Credentials"] = "true"
        response["Access-Control-Allow-Methods"] = "POST, OPTIONS"
        response["Access-Control-Allow-Headers"] = "Content-Type"

    def post(self, request):
        response = JsonResponse({"message": "Logged out successfully"})
        response.delete_cookie("csrftoken")
        response.delete_cookie(settings.SIMPLE_JWT.get('AUTH_COOKIE'))
        response.delete_cookie('refresh_token')

        response["Access-Control-Allow-Credentials"] = "true"

        return response