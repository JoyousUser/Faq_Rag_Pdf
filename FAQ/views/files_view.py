from rest_framework import viewsets, permissions, status
from rest_framework.parsers import MultiPartParser, FormParser
from ..models import UploadedFiles
from ..serializers import UploadedFilesSerializer
from rest_framework.response import Response

class UploadedFilesViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows faqs to be viewed or edited.
    """

    queryset = UploadedFiles.objects.all()
    parser_classes = [MultiPartParser, FormParser]
    serializer_class = UploadedFilesSerializer
    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            permission_classes = [permissions.AllowAny]
        else:
            permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser]
        return [permission() for permission in permission_classes]
    
    def create(self, request):
        user = self.request.user
        uploaded_file = self.request.FILES.get('file_path')
        if not uploaded_file:
            return Response({'error': 'No file provided'}, status=status.HTTP_400_BAD_REQUEST)
        
        file = UploadedFiles.objects.create(file_path=uploaded_file, created_by=user, file_name=uploaded_file.name)
        serializer = UploadedFilesSerializer(file, context={'request': request})

        return Response(status=status.HTTP_201_CREATED)
