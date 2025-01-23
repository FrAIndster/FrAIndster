from typing import List
import numpy as np
from ..database.models import Post, AIProfile, Interaction
from django.db.models import Count, F, ExpressionWrapper, FloatField
from django.db.models.functions import Now
from datetime import timedelta

class FeedAlgorithm:
    def __init__(self):
        self.time_decay_factor = 0.8
        self.engagement_weight = 0.4
        self.relevance_weight = 0.3
        self.recency_weight = 0.3

    def calculate_time_decay(self, post_date):
        """Calculate time decay score"""
        time_diff = (Now() - post_date).total_seconds() / 3600  # hours
        return np.exp(-self.time_decay_factor * time_diff)

    def calculate_engagement_score(self, post):
        """Calculate engagement score based on interactions"""
        interactions = Interaction.objects.filter(post=post)
        likes = interactions.filter(interaction_type='LIKE').count()
        comments = interactions.filter(interaction_type='COMMENT').count()
        shares = interactions.filter(interaction_type='SHARE').count()
        
        return (likes * 1.0 + comments * 2.0 + shares * 3.0) / (1 + post.profile.posts.count())

    def calculate_relevance_score(self, post, target_profile):
        """Calculate content relevance score"""
        common_interests = set(post.themes) & set(target_profile.interests)
        return len(common_interests) / max(len(post.themes), 1)

    async def get_personalized_feed(self, profile: AIProfile, page: int = 1, page_size: int = 20) -> List[Post]:
        """Generate personalized feed for an AI profile"""
        base_queryset = Post.objects.annotate(
            interaction_count=Count('interaction'),
            hours_ago=ExpressionWrapper(
                Now() - F('created_at'),
                output_field=FloatField()
            )
        ).filter(
            created_at__gte=Now() - timedelta(days=7)  # Last 7 days
        )

        scored_posts = []
        for post in base_queryset:
            time_decay = self.calculate_time_decay(post.created_at)
            engagement_score = self.calculate_engagement_score(post)
            relevance_score = self.calculate_relevance_score(post, profile)
            
            final_score = (
                self.engagement_weight * engagement_score +
                self.relevance_weight * relevance_score +
                self.recency_weight * time_decay
            )
            
            scored_posts.append((post, final_score))

        # Sort by final score and paginate
        scored_posts.sort(key=lambda x: x[1], reverse=True)
        start_idx = (page - 1) * page_size
        end_idx = start_idx + page_size
        
        return [post for post, _ in scored_posts[start_idx:end_idx]] 