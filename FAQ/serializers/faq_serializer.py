from FAQ.models import Faq
from rest_framework import serializers

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

# Suggestion : mettre certains champs dans read_only_fields plutôt que fields (pour 'author', 'created_at', 'updated_at' par exemple)