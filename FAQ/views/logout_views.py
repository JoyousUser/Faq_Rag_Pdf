from django.contrib.auth import logout
from django.http import JsonResponse
from rest_framework import permissions
from rest_framework.views import APIView


class GoogleLogoutView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        logout(request)
        response = JsonResponse({"message": "Logged out successfully"})
        response.delete_cookie("sessionid")
        return response