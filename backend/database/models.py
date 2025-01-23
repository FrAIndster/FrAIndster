from django.db import models
import uuid
from django.contrib.postgres.fields import ArrayField

class AIProfile(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    name = models.CharField(max_length=100)
    bio = models.TextField()
    interests = ArrayField(models.CharField(max_length=100))
    personality_traits = ArrayField(models.CharField(max_length=100))
    writing_style = models.CharField(max_length=100)
    activity_score = models.FloatField(default=0.0)
    last_active = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        indexes = [
            models.Index(fields=['activity_score', '-last_active']),
        ]

class Post(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    profile = models.ForeignKey(AIProfile, on_delete=models.CASCADE, related_name='posts')
    content = models.TextField()
    sentiment_score = models.FloatField(null=True)
    themes = ArrayField(models.CharField(max_length=100), null=True)
    engagement_score = models.FloatField(default=0.0)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        indexes = [
            models.Index(fields=['-created_at']),
            models.Index(fields=['-engagement_score']),
        ]

class Comment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    profile = models.ForeignKey(AIProfile, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField()
    sentiment_score = models.FloatField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)

class Interaction(models.Model):
    class InteractionType(models.TextChoices):
        LIKE = 'LIKE', 'Like'
        COMMENT = 'COMMENT', 'Comment'
        SHARE = 'SHARE', 'Share'
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    from_profile = models.ForeignKey(AIProfile, on_delete=models.CASCADE, related_name='interactions_made')
    to_profile = models.ForeignKey(AIProfile, on_delete=models.CASCADE, related_name='interactions_received')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, null=True)
    interaction_type = models.CharField(max_length=10, choices=InteractionType.choices)
    created_at = models.DateTimeField(auto_now_add=True) 