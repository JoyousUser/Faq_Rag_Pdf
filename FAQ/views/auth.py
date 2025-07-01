from django.shortcuts import redirect
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response

from faq_project.settings import GOOGLE_CALLBACK_URL


class GoogleJWTAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        refresh = RefreshToken.for_user(user)

        access_token = str(refresh.access_token)
        refresh_token = str(refresh)

        return redirect(f"{GOOGLE_CALLBACK_URL}?access={access_token}&refresh={refresh_token}")

        # return Response({
        #     'access': str(refresh.access_token),
        #     'refresh': str(refresh),
        #     'user_id': user.id,
        #     'username': user.username,
        # })