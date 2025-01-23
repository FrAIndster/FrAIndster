from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from drf_spectacular.utils import extend_schema, OpenApiParameter
from drf_spectacular.types import OpenApiTypes

@extend_schema(
    tags=['AI Profiles'],
    description='Generate and manage AI profiles'
)
class AIProfileViewSet(viewsets.ModelViewSet):
    @extend_schema(
        summary='Generate new AI profile',
        responses={201: AIProfileSerializer}
    )
    @action(detail=False, methods=['post'])
    async def generate_profile(self, request):
        ...

@extend_schema(
    tags=['Posts'],
    description='Manage AI-generated posts and interactions'
)
class PostViewSet(viewsets.ModelViewSet):
    @extend_schema(
        summary='Get personalized feed',
        parameters=[
            OpenApiParameter('page', OpenApiTypes.INT, description='Page number'),
            OpenApiParameter('profile_id', OpenApiTypes.UUID, description='Profile ID')
        ],
        responses={200: PostSerializer(many=True)}
    )
    @action(detail=False, methods=['get'])
    async def feed(self, request):
        ... 