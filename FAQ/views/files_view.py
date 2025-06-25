from rest_framework import viewsets, permissions, authentication, status
from ..models import UploadedFiles, Faq
from ..serializers import UploadedFilesSerializer, FaqSerializer
from rest_framework.response import Response

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

