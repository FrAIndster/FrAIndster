import pytest
from django.test import TestCase
from ..ai_models.anthropic_integration import AnthropicAI
from ..database.models import AIProfile, Post, Interaction
from unittest.mock import patch

@pytest.mark.asyncio
class TestAIInteractions(TestCase):
    def setUp(self):
        self.anthropic_client = AnthropicAI('test_key')

    @patch('anthropic.Anthropic')
    async def test_profile_generation(self, mock_anthropic):
        # Mock response
        mock_anthropic.return_value.messages.create.return_value.content = [{
            'text': '{"name": "TestAI", "bio": "Test bio", "interests": ["testing"]}'
        }]
        
        profile_data = await self.anthropic_client.generate_profile()
        
        assert profile_data['name'] == 'TestAI'
        assert 'testing' in profile_data['interests']

    @patch('anthropic.Anthropic')
    async def test_post_creation(self, mock_anthropic):
        profile = await AIProfile.objects.acreate(
            name='TestAI',
            bio='Test bio',
            interests=['testing']
        )
        
        mock_anthropic.return_value.messages.create.return_value.content = [{
            'text': 'Test post content'
        }]
        
        post_content = await self.anthropic_client.create_post(profile.to_dict())
        
        assert 'Test post content' in post_content 