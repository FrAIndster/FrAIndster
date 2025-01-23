from django.contrib.auth.models import AbstractUser
from django.db import models
import uuid

class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    email = models.EmailField(unique=True)
    is_researcher = models.BooleanField(default=False)
    api_key = models.UUIDField(default=uuid.uuid4, unique=True)
    
    class Meta:
        indexes = [
            models.Index(fields=['email']),
            models.Index(fields=['api_key']),
        ] 