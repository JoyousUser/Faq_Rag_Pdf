from django.shortcuts import render
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework import permissions, viewsets, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from rest_framework import authentication
from .serializers import UserSerializer, FaqSerializer, UploadedFilesSerializer
from .models import Faq, UploadedFiles, History

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

class LoginView(APIView):
    permission_classes = [permissions.AllowAny]
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)
        if user:
            token = Token.objects.get_or_create(user=user)[0]
            return Response({'token': token.key})
        return Response({'error': 'Invalid Credentials'}, status=status.HTTP_401_UNAUTHORIZED)

class LogoutView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [authentication.TokenAuthentication]
    def post(self, request):
        request.user.auth_token.delete()
        return Response(data={'message': 'Logged out successfully'},status=status.HTTP_200_OK)    
    
class FaqViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows faqs to be viewed or edited.
    """
    authentication_classes = [authentication.TokenAuthentication]
    queryset = Faq.objects.all()
    serializer_class = FaqSerializer

    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        if self.action == 'create':
            permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser]
        elif self.action in ['list', 'retrieve']:
            permission_classes = [permissions.AllowAny]
        else:
            permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser]
        return [permission() for permission in permission_classes]

    def perform_create(self, request):
        user = request.user
        faq = Faq.objects.create(author=user, question=request.data.get('question'), answer=request.data.get('answer'), generation=request.data.get('generation'))
        serializer = FaqSerializer(faq, context={'request': request})
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    

class UploadedFilesViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows faqs to be viewed or edited.
    """
    authentication_classes = [authentication.TokenAuthentication]
    queryset = UploadedFiles.objects.all()
    serializer_class = UploadedFilesSerializer

    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        if self.action == 'create':
            permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser]
        elif self.action in ['list', 'retrieve']:
            permission_classes = [permissions.AllowAny]
        else:
            permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser]
        return [permission() for permission in permission_classes]

    def perform_create(self, request):
        user = request.user
        faq = Faq.objects.create(author=user, question=request.data.get('question'), answer=request.data.get('answer'), generation=request.data.get('generation'))
        serializer = FaqSerializer(faq, context={'request': request})
        return Response(serializer.data, status=status.HTTP_201_CREATED)

