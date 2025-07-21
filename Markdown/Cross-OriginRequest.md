## Cross-Origin Resource Sharing (CORS)

Par défaut, la communication entre le frontend et le backend bloque certains mécanismes.
Dans mon cas, ma requête axios qui transmettait les tokens JWT était bloquée et ma view Django n'était jamais appelé, avec pour
raison "Blocage d’une requête multiorigines (Cross-Origin Request) : la politique « Same Origin » ne permet pas de consulter la ressource distante"

La solution est d'installer le package CORS et de le configurer proprement.

pip install django-cors-headers

Dans Settings, quelques lignes à ajouter :
``` python
if DEBUG:
    CORS_ALLOWED_ORIGINS = [
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost8000",
    ]
else:
    CORS_ALLOWED_ORIGINS = [
        "https://faq-rag-pdf.vercel.app",   # à modifier pour le vrai nom de domaine une fois en prod
    ]
```

Dans INSTALLED_APPS, à mettre tout en haut :
``` python
INSTALLED_APPS = [
    ...,
    'corsheaders.middleware.CorsMiddleware',
    ...,
]
```
Et dans Middleware, à mettre sous 'django.middleware.security.SecurityMiddleware' :
``` python
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    ...
]
```
