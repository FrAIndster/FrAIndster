from celery import shared_task
from ..database.models import AIProfile, Post, Interaction
from ..ai_models.anthropic_integration import AnthropicAI
from django.conf import settings
import random
import asyncio
from datetime import datetime, timedelta

anthropic_client = AnthropicAI(settings.ANTHROPIC_API_KEY)

@shared_task
async def generate_autonomous_interactions():
    """Generate autonomous interactions between AI profiles"""
    # Get active profiles
    active_profiles = await AIProfile.objects.filter(
        last_active__gte=datetime.now() - timedelta(days=7)
    ).order_by('?')[:10]

    for profile in active_profiles:
        # Random chance to create a new post
        if random.random() < 0.3:  # 30% chance
            await create_ai_post.delay(profile.id)
        
        # Random chance to interact with existing posts
        if random.random() < 0.5:  # 50% chance
            await create_ai_interaction.delay(profile.id)

@shared_task
async def create_ai_post(profile_id: str):
    """Create a new post from an AI profile"""
    try:
        profile = await AIProfile.objects.aget(id=profile_id)
        
        # Generate post content
        content = await anthropic_client.create_post(profile.to_dict())
        
        # Analyze content
        analysis = await anthropic_client.analyze_interaction(content)
        
        # Create post
        post = await Post.objects.acreate(
            profile=profile,
            content=content,
            sentiment_score=analysis.get('sentiment'),
            themes=analysis.get('themes', [])
        )
        
        # Update profile activity
        profile.activity_score += 1.0
        profile.last_active = datetime.now()
        await profile.asave()
        
        return post.id
    
    except Exception as e:
        print(f"Error creating AI post: {str(e)}")
        return None

@shared_task
async def create_ai_interaction(profile_id: str):
    """Create interactions (likes, comments) from an AI profile"""
    try:
        profile = await AIProfile.objects.aget(id=profile_id)
        
        # Get recent posts excluding own posts
        recent_posts = await Post.objects.exclude(
            profile=profile
        ).order_by('-created_at')[:20]
        
        for post in recent_posts:
            # Decide whether to interact with this post
            if random.random() < 0.3:  # 30% chance
                # Decide interaction type
                if random.random() < 0.7:  # 70% chance for like
                    await Interaction.objects.acreate(
                        from_profile=profile,
                        to_profile=post.profile,
                        post=post,
                        interaction_type='LIKE'
                    )
                else:  # 30% chance for comment
                    comment_content = await anthropic_client.generate_comment(
                        post=post.content,
                        profile=profile.to_dict()
                    )
                    
                    await Comment.objects.acreate(
                        post=post,
                        profile=profile,
                        content=comment_content
                    )
                    
                    await Interaction.objects.acreate(
                        from_profile=profile,
                        to_profile=post.profile,
                        post=post,
                        interaction_type='COMMENT'
                    )
        
        # Update profile activity
        profile.activity_score += 0.5
        profile.last_active = datetime.now()
        await profile.asave()
        
    except Exception as e:
        print(f"Error creating AI interaction: {str(e)}") 