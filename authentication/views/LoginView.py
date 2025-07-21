from django.contrib.auth import authenticate
from django.http import JsonResponse
from django.middleware import csrf
from django.shortcuts import redirect
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response

from faq_project import settings
from faq_project.settings import GOOGLE_CALLBACK_URL


class GoogleJWTAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        response = Response()
        user = request.user
        refresh = RefreshToken.for_user(user)
        csrf_token = csrf.get_token(request)
        access_token = str(refresh.access_token)
        refresh_token = str(refresh)

        response = JsonResponse({
            "message": "Successfully logged in via Google",
            "csrf_token": csrf_token,
        })
        response.status_code = 302
        response["Location"] = "http://localhost:5173/"
        response["Access-Control-Allow-Credentials"] = "true"

        cookie_name = settings.SIMPLE_JWT.get('AUTH_COOKIE')
        cookie_secure = settings.SIMPLE_JWT.get('AUTH_COOKIE_SECURE')
        cookie_httponly = settings.SIMPLE_JWT.get('AUTH_COOKIE_HTTP_ONLY')
        cookie_samesite = settings.SIMPLE_JWT.get('AUTH_COOKIE_SAMESITE')
        cookie_path = settings.SIMPLE_JWT.get('AUTH_COOKIE_PATH')


        # Définition des cookies
        response.set_cookie(
            key=cookie_name,
            value=access_token,
            httponly=cookie_httponly,
            secure=cookie_secure,
            samesite=cookie_samesite,
            path=cookie_path,
            expires = settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME'],
        )

        response.set_cookie(
            key='refresh_token',
            value=refresh_token,
            httponly=cookie_httponly,
            secure=cookie_secure,
            samesite=cookie_samesite,
            path=cookie_path,
            expires = settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME'],
        )

        response.set_cookie(
            key='csrftoken',
            value=csrf_token,
            httponly=False,  # Important : False pour que le frontend puisse le lire
            secure=cookie_secure,
            samesite=cookie_samesite,
            path=cookie_path
        )

        return response




#============================================================   old version (functional)

    # def get(self, request):
    #     user = request.user
    #     refresh = RefreshToken.for_user(user)
    #
    #     access_token = str(refresh.access_token)
    #     refresh_token = str(refresh)
    #
    #     # return redirect(f"{GOOGLE_CALLBACK_URL}?access={access_token}&refresh={refresh_token}")       ## Renvoie les infos dans l'URL -> pas propre et pas très sûr
    #
    #     return JsonResponse({
    #         'access': str(refresh.access_token),
    #         'refresh': str(refresh),
    #         'user_id': user.id,
    #         'username': user.username,
    #     })