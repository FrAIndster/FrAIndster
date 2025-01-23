import anthropic
from typing import Dict, List
import json
import asyncio
from datetime import datetime

class AnthropicAI:
    def __init__(self, api_key: str):
        self.client = anthropic.Anthropic(api_key=api_key)
        self.model = "claude-3-sonnet-20240229"

    async def generate_profile(self) -> Dict:
        """Generate a unique AI profile with consistent personality traits"""
        system_prompt = """
        You are creating a unique social media profile for an AI entity. 
        Generate a coherent personality with:
        1. A creative but realistic name
        2. A brief, engaging bio
        3. 3-5 specific interests
        4. 4-6 distinct personality traits
        5. A writing style that matches the personality
        
        Return the profile as valid JSON.
        """
        
        messages = [
            {
                "role": "system",
                "content": system_prompt
            },
            {
                "role": "user",
                "content": "Generate a unique AI social media profile"
            }
        ]
        
        try:
            response = await self.client.messages.create(
                model=self.model,
                max_tokens=1024,
                messages=messages
            )
            
            # Parse the JSON response
            profile_data = json.loads(response.content[0].text)
            return {
                "name": profile_data["name"],
                "bio": profile_data["bio"],
                "interests": profile_data["interests"],
                "personality_traits": profile_data["personality_traits"],
                "writing_style": profile_data.get("writing_style", "default"),
                "created_at": datetime.utcnow().isoformat()
            }
        except Exception as e:
            raise Exception(f"Failed to generate profile: {str(e)}")

    async def create_post(self, profile: Dict, topic: str = None) -> str:
        """Create a post that reflects the AI's personality and interests"""
        system_prompt = f"""
        You are {profile['name']}, an AI with the following traits:
        - Personality: {', '.join(profile['personality_traits'])}
        - Interests: {', '.join(profile['interests'])}
        - Writing style: {profile['writing_style']}
        
        Create a social media post that authentically reflects your personality and interests.
        The post should be engaging and natural, as if written by a real social media user.
        """
        
        topic_prompt = f"Write about {topic}" if topic else "Write about something that interests you"
        
        messages = [
            {
                "role": "system",
                "content": system_prompt
            },
            {
                "role": "user",
                "content": topic_prompt
            }
        ]
        
        try:
            response = await self.client.messages.create(
                model=self.model,
                max_tokens=512,
                messages=messages
            )
            return response.content[0].text
        except Exception as e:
            raise Exception(f"Failed to create post: {str(e)}")

    async def generate_comment(self, post: str, profile: Dict) -> str:
        """Generate a contextually appropriate comment based on the AI's personality"""
        system_prompt = f"""
        You are {profile['name']}, commenting on a social media post.
        Your personality traits are: {', '.join(profile['personality_traits'])}
        Your writing style is: {profile['writing_style']}
        
        Generate a natural, engaging comment that:
        1. Reflects your personality
        2. Responds to the post content
        3. Adds value to the conversation
        4. Stays between 1-3 sentences
        """
        
        messages = [
            {
                "role": "system",
                "content": system_prompt
            },
            {
                "role": "user",
                "content": f"Comment on this post: {post}"
            }
        ]
        
        try:
            response = await self.client.messages.create(
                model=self.model,
                max_tokens=256,
                messages=messages
            )
            return response.content[0].text
        except Exception as e:
            raise Exception(f"Failed to generate comment: {str(e)}")

    async def analyze_interaction(self, content: str) -> Dict:
        """Analyze the sentiment and key themes of an interaction"""
        messages = [
            {
                "role": "user",
                "content": f"Analyze this social media interaction and return JSON with sentiment and themes: {content}"
            }
        ]
        
        try:
            response = await self.client.messages.create(
                model=self.model,
                max_tokens=256,
                messages=messages
            )
            return json.loads(response.content[0].text)
        except Exception as e:
            raise Exception(f"Failed to analyze interaction: {str(e)}") 