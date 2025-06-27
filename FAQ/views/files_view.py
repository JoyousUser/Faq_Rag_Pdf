from rest_framework import viewsets, permissions, authentication, status
from rest_framework.parsers import MultiPartParser, FormParser
from ..models import UploadedFiles
from ..serializers import UploadedFilesSerializer
from rest_framework.response import Response

class UploadedFilesViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows faqs to be viewed or edited.
    """
    parser_classes = [MultiPartParser, FormParser]
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
        uploaded_file = request.FILES.get('file_path')
        if not uploaded_file:
            return Response({'error': 'No file provided'}, status=status.HTTP_400_BAD_REQUEST)
        
        file = UploadedFiles.objects.create(file_path=uploaded_file, created_by=user)
        serializer = UploadedFilesSerializer(file, context={'request': request})
         
        return Response(status=status.HTTP_201_CREATED)

