from FAQ.models import UploadedFiles
from rest_framework import serializers

class UploadedFilesSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = UploadedFiles
        fields = ['file_path']
        read_only_fields = ['created_by', 'created_at']

