from django.db import models

class FAQGenerator(models.Model):
    model_name = models.CharField(max_length=100, default='GPT-3.5 Turbo')
    ai_prompt = models.TextField(default='Generate a FAQ based on the provided question and answer.')

    #placeholder autocompleted, classe abstraite où definir le model d'ia a utiliser

    class Meta:
        abstract = True