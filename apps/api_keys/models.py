from django.db import models
import secrets
# Create your models here.

class APIKey(models.Model):
    project= models.ForeignKey(
        'project.Project',
        on_delete = models.CASCADE,
        related_name = 'api_keys',
    )
    name = models.CharField(max_length=100)
    key = models.CharField(max_length=255, unique=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True,editable=False)
    last_used_at = models.DateTimeField(null=True, blank=True)


    @staticmethod
    def generate_key():
        return f"gf_live_{secrets.token_urlsafe(32)}"
