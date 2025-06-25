# Intégration du JWT avec SimpleJWT (via DRF)


## Etape 1 : installation
pip install djangorestframework-simplejwt
pip freeze > requirements.txt

## Etape 2 : configuration des Settings
from datetime import timedelta  -->  pour gérer la durée de vie des tokens

REST_FRAMEWORK = {  
    'DEFAULT_AUTHENTICATION_CLASSES': (  
        'rest_framework_simplejwt.authentication.JWTAuthentication',    # Auth via token (frontend)  
        'rest_framework.authentication.SessionAuthentication',          # Auth via login Google / Django  
    )  
}  
-->  DRF regarde dans l'ordre chaque classe listée dans DEFAULT_AUTHENTICATION_CLASSES
Il essaie d'authentifier la requête avec cette méthode. Si ça échoue sans erreur critique,
il essaie la suivante.
Si aucune n'authentifie la requête, alors request.user sera AnonymousUser.  
Cela permet de combiner JWT (pour les appels d'API depuis React) et SessionAuthentication  
(pour les utilisateurs connectés via Google / Django)


SIMPLE_JWT = {  
    'ACCESS_TOKEN_LIFETIME': timedelta(hours=1),    # Durée de vie du token  
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),    # Durée de vie du refresh token  
    'AUTH_HEADER_TYPES': ('Bearer',),               # Préfixe du header 'Authorization'  
    'AUTH_HEADER_NAME': 'HTTP_AUTHORIZATION',       # Nom de l'en-tête HTTP à analyser. En WSGI, 'Authorization' devient 'HTTP_AUTHORIZATION'  
    'USER_ID_FIELD': 'id',                          # Nom du champ du User utilisé pour stocker son ID dans le token  
    'USER_ID_CLAIM': 'user_id',                     # Nom de la _claim_ JWT utilisée pour stocker le user_id  
    'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt.tokens.AccessToken',),     # classe pour créer les access tokens  
    'TOKEN_TYPE_CLAIM': 'token_type',               # Indique le type de token (access ou refresh) dans le payload  
    'JTI_CLAIM': 'jti',                             # ID unique au token (permet de faire du blacklist ou logout)  
    'ALGORITHM': 'HS256',                           # Algo de signature  
    'SIGNING_KEY': SECRET_KEY,                      # Clef secrète pour signer le JWT (ne jamais montrer publiquement)  
    'LEEWAY': 0,                                    # Tolérance en secondes dans le calcul des dates  
}


### Optionnel : personnaliser les données contenues dans le token
- Créer le Serializer (FAQ/serializers/CustomTokenSerializer.py) :


``` python
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # ✅ Ajoute ici les infos personnalisées
        token['email'] = user.email
        token['username'] = user.username
        token['is_admin'] = getattr(user.profile, 'is_admin', False)

        return token
```
- Créer la view associée pour le JWT (FAQ/views/CustomTokenView.py)
``` python
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import CustomTokenObtainPairSerializer

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer
```
- Et enfin, la route (FAQ/urls/CustomTokenUrl):
``` python
from django.urls import path
from .views import CustomTokenObtainPairView
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('api/token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
```

## Etape 3 : Configurer les URLs d'accès aux tokens
Dans FAQ.urls, rajouter dans urlpatterns :  
``` python
urlpatterns = [...,  
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain pair'),  
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh')  
]
```
Et dans faq_project.urls, ne pas oublier de rajouter la route vers FAQ.urls :
``` python
urlpatterns = [...,
    path('', include('FAQ.urls')),
]
```

## Etape 4 : tester la création du token
- se connecter sur la page http://127.0.0.1:8000/api/token/
- en utilisant un logiciel comme Insomnia ou Postman :
        - Méthode POST
        - Body JSON : {
                        "username": "nom_utilisateur",
                        "password": "mot_de_passe"
                      }
- Vérifier la création du token d'access et du token de refresh