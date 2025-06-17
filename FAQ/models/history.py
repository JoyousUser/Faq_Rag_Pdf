from django.db import models
from django.contrib.auth.models import User

class History(models.Model):

    visited = models.CharField(max_length=255)
    # à récupérer depuis la view avec : request.get_full_path()
    faq_id = models.ForeignKey('faq.Faq', on_delete=models.CASCADE, related_name='histories')
    visited_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.faq_id.question} by {self.created_by.username} on {self.created_at.strftime('%Y-%m-%d %H:%M:%S')}"
        #autocompleted, je ne sais pas encore ce qu'on veux pouvoir récup de l'historique.

