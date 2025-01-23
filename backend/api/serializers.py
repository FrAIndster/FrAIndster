from rest_framework import serializers
from ..database.models import AIProfile, Post, Comment, Interaction

class AIProfileSerializer(serializers.ModelSerializer):
    engagement_rate = serializers.SerializerMethodField()
    post_count = serializers.SerializerMethodField()
    
    class Meta:
        model = AIProfile
        fields = [
            'id', 'name', 'bio', 'interests', 'personality_traits',
            'writing_style', 'activity_score', 'last_active',
            'created_at', 'engagement_rate', 'post_count'
        ]
    
    def get_engagement_rate(self, obj):
        total_posts = obj.posts.count()
        if total_posts == 0:
            return 0.0
        total_interactions = Interaction.objects.filter(to_profile=obj).count()
        return round(total_interactions / total_posts, 2)
    
    def get_post_count(self, obj):
        return obj.posts.count()

class CommentSerializer(serializers.ModelSerializer):
    profile = AIProfileSerializer(read_only=True)
    
    class Meta:
        model = Comment
        fields = ['id', 'profile', 'content', 'sentiment_score', 'created_at']

class PostSerializer(serializers.ModelSerializer):
    profile = AIProfileSerializer(read_only=True)
    comments = CommentSerializer(many=True, read_only=True)
    interaction_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Post
        fields = [
            'id', 'profile', 'content', 'sentiment_score', 'themes',
            'engagement_score', 'created_at', 'comments', 'interaction_count'
        ]
    
    def get_interaction_count(self, obj):
        return Interaction.objects.filter(post=obj).count() 