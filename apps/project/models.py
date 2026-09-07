from django.db import models
from django.conf import settings

class Project(models.Model):
    owner = models.ForeignKey(
         settings.AUTH_USER_MODEL,
         related_name='projects', 
         on_delete=models.CASCADE)

    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True,editable=False)
    updated_at = models.DateTimeField(auto_now=True)
    