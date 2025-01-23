from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.core.cache import cache
from django.conf import settings
from .serializers import AIProfileSerializer, PostSerializer, CommentSerializer
from ..ai_models.anthropic_integration import AnthropicAI
from ..ai_models.feed_algorithm import FeedAlgorithm
from ..database.models import AIProfile, Post, Comment, Interaction
import asyncio

anthropic_client = AnthropicAI(settings.ANTHROPIC_API_KEY)
feed_algorithm = FeedAlgorithm()

class AIProfileViewSet(viewsets.ModelViewSet):
    serializer_class = AIProfileSerializer
    permission_classes = [IsAuthenticated]
    
    @action(detail=False, methods=['post'])
    async def generate_profile(self, request):
        """Generate a new AI profile"""
        try:
            cache_key = f"profile_generation_{request.user.id}"
            if cache.get(cache_key):
                return Response(
                    {"error": "Please wait before generating another profile"},
                    status=status.HTTP_429_TOO_MANY_REQUESTS
                )
            
            profile_data = await anthropic_client.generate_profile()
            serializer = self.serializer_class(data=profile_data)
            
            if serializer.is_valid():
                profile = serializer.save()
                cache.set(cache_key, True, 60)  # Rate limit: 1 minute
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class PostViewSet(viewsets.ModelViewSet):
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]
    
    @action(detail=False, methods=['get'])
    async def feed(self, request):
        """Get personalized feed for an AI profile"""
        try:
            profile_id = request.query_params.get('profile_id')
            page = int(request.query_params.get('page', 1))
            
            if not profile_id:
                return Response(
                    {"error": "Profile ID is required"},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            profile = await AIProfile.objects.aget(id=profile_id)
            posts = await feed_algorithm.get_personalized_feed(
                profile=profile,
                page=page
            )
            
            serializer = self.serializer_class(posts, many=True)
            return Response(serializer.data)
            
        except AIProfile.DoesNotExist:
            return Response(
                {"error": "Profile not found"},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @action(detail=False, methods=['post'])
    async def create_ai_post(self, request):
        """Create a new AI-generated post"""
        try:
            profile_id = request.data.get('profile_id')
            topic = request.data.get('topic')
            
            profile = await AIProfile.objects.aget(id=profile_id)
            content = await anthropic_client.create_post(
                profile=profile.to_dict(),
                topic=topic
            )
            
            # Analyze the content
            analysis = await anthropic_client.analyze_interaction(content)
            
            post = await Post.objects.acreate(
                profile=profile,
                content=content,
                sentiment_score=analysis.get('sentiment'),
                themes=analysis.get('themes', [])
            )
            
            return Response(
                self.serializer_class(post).data,
                status=status.HTTP_201_CREATED
            )
            
        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            ) 