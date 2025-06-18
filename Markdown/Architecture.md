# Suggestion d'architecture propre et structurée


ProjectFAQ/
├── backend/
│   ├── manage.py
│   ├── core/                        # Projet Django
│   │   ├── __init__.py
│   │   ├── settings.py
│   │   ├── urls.py                  # Inclut les routes DRF et social-auth
│   │   ├── asgi.py
│   │   └── wsgi.py
│
│   ├── faq/                         # App principale
│   │   ├── __init__.py
│   │   ├── admin.py
│   │   ├── apps.py
│   │   ├── models/
│   │   │   ├── __init__.py          # Centralise les exports
│   │   │   ├── FAQEntry.py
│   │   │   ├── UploadedPDF.py
│   │   │   ├── VisitLog.py
│   │   │   └── Profile.py
│   │   ├── serializers/
│   │   │   ├── __init__.py
│   │   │   ├── faq_entry.py
│   │   │   ├── uploaded_pdf.py
│   │   │   └── visit_log.py
│   │   ├── views/
│   │   │   ├── __init__.py
│   │   │   ├── faq_entry.py
│   │   │   ├── uploaded_pdf.py
│   │   │   └── visit_log.py
│   │   ├── urls.py                  # Route les ViewSets
│   │   ├── permissions.py           # (optionnel) accès restreint admin/user
│   │   ├── services/
│   │   │   └── ia_generation.py     # (ou rag_pipeline.py, etc.)
│   │   ├── signals.py               # pour créer le Profile automatiquement
│   │   └── templates/               # si tu as des vues HTML
│
│   ├── media/                       # fichiers PDF uploadés
│   └── static/                      # fichiers statiques (collectstatic)
│
├── docker-compose.yml
├── Dockerfile
├── .env
└── requirements.txt