from django.contrib.auth.models import User
from FAQ.models import Faq, UploadedFiles, History
from rest_framework import serializers


class UserSerializer(serializers.HyperlinkedModelSerializer):
    faqs = serializers.HyperlinkedRelatedField(
        many=True,
        read_only=True,
        view_name='faq-detail',
        source='faq_set',
        
    )
    class Meta:
        model = User    
        fields = ['id', 'url', 'username', 'first_name', 'last_name', 'email', 'is_staff', 'faqs']
    # json example of a user
    # {
    #     "id": 1,
    #     "username": "testuser",
    #     "password": "testuser",
    #     "first_name": "",
    #     "last_name": "",
    #     "email": "test@example.com",
    #     "is_staff": false
    # }
    

class FaqSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Faq
        fields = ['author', 'updated_at', 'created_at', 'question', 'answer', 'generation']
    # json example of an FAQ
    # {
    #     "id": 1,
    #     "author": 1,
    #     "question": "What is Django?",
    #     "answer": "Django is a high-level Python Web framework that encourages rapid development and clean, pragmatic design.",
    #     "generation": "Manual"
    # }

class UploadedFilesSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = UploadedFiles
        fields = ['file_path', 'created_at', 'created_by']

class HistorySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = History
        fields = ['visisted', 'faq_id', 'visited_by', 'created_at']
