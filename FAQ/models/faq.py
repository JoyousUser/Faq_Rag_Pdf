from django.db import models
from django.contrib.auth.models import User

class Faq(models.Model):

    generation_choices = [
        ('Manual', 'Manual'),
        ('AI', 'AI'),
    ]

    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    validated = models.BooleanField(default=False)
    question = models.TextField()
    answer = models.TextField()
    generation = models.CharField(choices=generation_choices, max_length=6, default='AI')


    def __str__(self):
        return f"{self.question} - {self.answer} ({self.generation})"



