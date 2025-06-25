from rest_framework.views import APIView
from rest_framework import permissions, status, authentication
from rest_framework.response import Response
from rest_framework.authtoken.models import Token

class LogoutView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [authentication.TokenAuthentication]
    def post(self, request):
        request.user.auth_token.delete()
        return Response(data={'message': 'Logged out successfully'},status=status.HTTP_200_OK)    
    