from django.db import models
from django.contrib.auth.models import User

class UploadedFiles(models.Model):

    file_path = models.FileField(upload_to='uploaded_files/')
    #upload le fichier vers le dossier MEDIA_ROOT/uploaded_files/ et enregistre son chemin relatif en bdd
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"File: {self.file_path.name} uploaded by {self.created_by.username} on {self.created_at.strftime('%Y-%m-%d %H:%M:%S')}"
        #affiche le nom du fichier, l'utilisateur qui l'a uploadé et la date de création

