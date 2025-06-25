from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework.response import Response 
from rest_framework import viewsets, permissions, authentication
from ..serializers import UserSerializer


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser]
    authentication_classes = [authentication.TokenAuthentication]
    def create(self, request):
        user = User.objects.create_user(username=request.data.get('username'), password=request.data.get('password'))
        user.save()
        token = Token.objects.create(user=user)
        return Response({'token': token.key})