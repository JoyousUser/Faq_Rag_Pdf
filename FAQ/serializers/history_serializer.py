from FAQ.models import History
from rest_framework import serializers

class HistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = History
        fields = ['visited', 'faq_id', 'visited_by', 'created_at']
