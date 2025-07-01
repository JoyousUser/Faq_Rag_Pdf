from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

class ProtectedView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        ## Teste du headers - Vérification des tokens
        print("====== HEADERS =====")
        for key, value in request.headers.items():
            print(f"{key}: {value}")
        print("========================")

        return Response({"message": f"Hello {request.user.username}, you are authenticated!"})
