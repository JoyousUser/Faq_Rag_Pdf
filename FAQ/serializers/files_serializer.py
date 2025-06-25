from FAQ.models import UploadedFiles
from rest_framework import serializers

class UploadedFilesSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = UploadedFiles
        fields = ['file_path', 'created_at', 'created_by']