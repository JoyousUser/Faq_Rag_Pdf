from django.db import models
from django.contrib.auth import get_user_model

# Create your models here.

class VisitLog(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    url = models.CharField(max_length=2048)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} - {self.url} - {self.timestamp}"