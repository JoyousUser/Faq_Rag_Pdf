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
    queryset = Faq.objects.all()
    serializer_class = FaqSerializer
    Faq_ai_generator = FAQGenerator()

    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        if self.action in ['list', 'retrieve']:
            permission_classes = [permissions.AllowAny]
        else:
            permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser]
        return [permission() for permission in permission_classes]

    def perform_create(self, request):
        user = request.user
        faq = Faq.objects.create(author=user, question=request.data.get('question'), answer=request.data.get('answer'), generation='Manual')
        serializer = FaqSerializer(faq, context={'request': request})
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    
    @action(detail=True, methods=["get"], url_path="generate", permission_classes=[permissions.IsAuthenticated, permissions.IsAdminUser])
    def generate(self, request, *args, **kwargs):
        """
        Method to generate an FAQ using AI. \n
        This method doesn't automatically save the FAQs to do that database, they need to be manually saved one by one, on the client side.
        """
        pk = self.kwargs.get("pk")
        # ai_model = request.data['ai_model']

        # Checking if file exists
        try:
            uploaded_file = UploadedFiles.objects.get(id=pk)
        except Exception as e:
            return Response({"message": "File not found"}, status=status.HTTP_404_NOT_FOUND)
        
        # Generating FAQs by Llama3
        try:
            # if ai_model:
            #     print(ai_model)
            #     self.Faq_ai_generator.ai_model = ai_model
            ai_generated_faqs = self.Faq_ai_generator.generate_ai_prompt(uploaded_file=str(uploaded_file.file_path))
        except Exception as e:
            print(e)
            return Response({"message": f"Server side error while generating the FAQs or AI model  is not available."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        return Response(ai_generated_faqs, status=status.HTTP_200_OK)
        
    
# Méthode perform_create peut être simplifiée :
# def perform_create(self, serializer):
#     serializer.save(author=self.request.user)
#
# → Ce code :
#     utilise le serializer comme Django/DRF le souhaite,
#     affecte correctement l’auteur via request.user.
