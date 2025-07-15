from FAQ.models import UploadedFiles
from rest_framework import serializers

class UploadedFilesSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = UploadedFiles
        fields = ['id', 'file_name','file_path', 'created_at', 'created_by']

