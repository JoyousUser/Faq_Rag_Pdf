from FAQ.models import Faq
from rest_framework import serializers

class FaqSerializer(serializers.ModelSerializer):
    file = serializers.SerializerMethodField()
    class Meta:
        model = Faq
        fields = ['id', 'author', 'updated_at', 'created_at', 'question', 'answer', 'generation', 'file']
        read_only_fields = ['author', 'created_at', 'updated_at']

    def get_file(self, obj):
        from . import UploadedFilesSerializer  
        if obj.file:
            return UploadedFilesSerializer(obj.file).data
        return None
    
    def get_author(self, obj):
        from . import UserSerializer
        if obj.author: 
            return UserSerializer(obj.author).data
        return None
    # json example of an FAQ
    # {
    #     "id": 1,
    #     "author": 1,
    #     "question": "What is Django?",
    #     "answer": "Django is a high-level Python Web framework that encourages rapid development and clean, pragmatic design.",
    #     "generation": "Manual"
    # }

# Suggestion : mettre certains champs dans read_only_fields plutôt que fields (pour 'author', 'created_at', 'updated_at' par exemple)