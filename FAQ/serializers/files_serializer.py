from FAQ.models import UploadedFiles
from rest_framework import serializers

class UploadedFilesSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = UploadedFiles
        fields = ['file_path', 'created_at', 'created_by']

# Suggestion : mettre certains champs dans read_only_fields plutôt que fields (pour 'created_at', 'updated_at' par exemple)