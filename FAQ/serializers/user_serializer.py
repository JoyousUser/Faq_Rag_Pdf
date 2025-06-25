from django.contrib.auth.models import User
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
    