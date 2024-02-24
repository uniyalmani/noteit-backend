from django.db import models
from uuid import uuid4
from auth_app.models import CustomUser as User
# from django.contrib.postgres.fields import JSONField
import json

class Note(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4)
    content = models.TextField()
    # content = JSONField()
    title = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    
    
    
    

