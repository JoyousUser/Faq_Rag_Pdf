from rest_framework import viewsets, permissions, authentication, status
from rest_framework.response import Response
from ..models import Faq
from ..serializers import FaqSerializer

class FaqViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows faqs to be viewed or edited.
    """
    queryset = Faq.objects.all()
    serializer_class = FaqSerializer

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
        faq = Faq.objects.create(author=user, question=request.data.get('question'), answer=request.data.get('answer'), generation=request.data.get('generation'))
        serializer = FaqSerializer(faq, context={'request': request})
        return Response(serializer.data, status=status.HTTP_201_CREATED)


# Méthode perform_create peut être simplifiée :
# def perform_create(self, serializer):
#     serializer.save(author=self.request.user)
#
# → Ce code :
#     utilise le serializer comme Django/DRF le souhaite,
#     affecte correctement l’auteur via request.user.
