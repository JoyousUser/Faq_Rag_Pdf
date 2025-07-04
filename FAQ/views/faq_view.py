from rest_framework import viewsets, permissions, authentication, status
from rest_framework.response import Response
from rest_framework.decorators import action
from ..models import Faq, UploadedFiles
from ..services import FAQGenerator
from ..serializers import FaqSerializer

class FaqViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows faqs to be viewed or edited.
    """
    authentication_classes = [authentication.TokenAuthentication]
    queryset = Faq.objects.all()
    serializer_class = FaqSerializer
    Faq_ai_generator = FAQGenerator()

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
        faq = Faq.objects.create(author=user, question=request.data.get('question'), answer=request.data.get('answer'), generation='Manual')
        serializer = FaqSerializer(faq, context={'request': request})
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    @action(detail=True, methods=["post"], url_path="generate", permission_classes=[permissions.IsAuthenticated, permissions.IsAdminUser])
    def generate(self, *args, **kwargs):
        """Method to generate an FAQ using AI"""
        pk = self.kwargs.get("pk")
        try:
            uploaded_file = UploadedFiles.objects.get(id=pk)
        except Exception as e:
            return Response({"message": "File not found"}, status=status.HTTP_404_NOT_FOUND)
        ai_generated_faqs = self.Faq_ai_generator.generate_ai_prompt(uploaded_file=str(uploaded_file.file_path))
        print(ai_generated_faqs)
        # if ai_generated_faqs:
        return Response(ai_generated_faqs, status=status.HTTP_200_OK)
        
        # return Response({"message": "Error while generating the FAQ"},status=status.HTTP_500_INTERNAL_SERVER_ERROR)