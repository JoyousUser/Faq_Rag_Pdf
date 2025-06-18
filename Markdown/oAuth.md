=== Comment mettre en place une authentification via compte Google grâce à oAuth ===

- Installer le module decouple : pip install python-decouple
(Attention : "pip install decouple" existe aussi, mais ça fait tout buguer)
Le module est dans le requirements.txt
- pip install social-auth-app-django (pour l'authentification oAuth de Google)
- URL de connexion via compte Google : http://localhost:8000/auth/login/google-oauth2/  pour se connecter


# Dans Settings :
- importer le module decouple
- utiliser la commande "config" pour renvoyer la recherche des infos brutes dans le .env
  SECRET_KEY = config('SECRET_KEY')
  DEBUG = config('DEBUG', default=False, cast=bool)
  ALLOWED_HOSTS = config('ALLOWED_HOSTS', cast=Csv())
- INSTALLED_APP = [..., 'social_django']
- MIDDLEWARE = [..., 'social_django.middleware.SocialAuthExceptionMiddleware']
- AUTHENTICATION_BACKENDS = [
    'social_core.backends.google.GoogleOAuth2',
    'django.contrib.auth.backends.ModelBackend',
]
- AUTHENTICATION_BACKENDS = [
    'social_core.backends.google.GoogleOAuth2',
    'django.contrib.auth.backends.ModelBackend',
]

== Clef et clef secrète pour l'authentification vers l'API de Google ==
(infos dans le .env)
SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = config('SOCIAL_AUTH_GOOGLE_OAUTH2_KEY')
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = config('SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET')

==> URL de redirection suite à connexion / déconnexion
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'

# Dans faq_project/urls.py
urlpatterns = [ ... , path('auth/', include('social_django.urls', namespace='social')),]
--> créé les endpoints /auth/login/google-oauth2/   et   /complete/google-oauth2/