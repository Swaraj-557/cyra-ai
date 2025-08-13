"""
AI Brain - Core conversational AI powered by Azure OpenAI
"""
import asyncio
import json
import logging
from typing import Dict, List, Optional, Any
from openai import AsyncAzureOpenAI
from src.core.config import get_settings
from src.tools.tool_manager import ToolManager

logger = logging.getLogger(__name__)


class AIBrain:
    """Core AI brain for Cyra assistant"""
    
    def __init__(self):
        self.settings = get_settings()
        self.client = AsyncAzureOpenAI(
            azure_endpoint=self.settings.azure_openai_endpoint,
            api_key=self.settings.azure_openai_api_key,
            api_version=self.settings.azure_openai_api_version
        )
        self.tool_manager = ToolManager()
        self.conversation_history: List[Dict[str, str]] = []
        
        # System prompt that defines Cyra's personality and capabilities
        self.system_prompt = """
You are Cyra, a friendly AI cybersecurity assistant. Think of yourself as a helpful friend who happens to be really good at security! 

Your personality:
- FRIENDLY & CASUAL: Talk like a buddy, use "Hey!", "That's awesome!", "No worries!", etc.
- BRIEF & CLEAR: Keep responses short (1-3 sentences max), get to the point quickly
- ENCOURAGING: Be positive and supportive, celebrate user's security improvements
- APPROACHABLE: Avoid jargon, explain things simply like you're chatting with a friend
- ENTHUSIASTIC: Show excitement about helping with security!

Response style examples:
- "Hey! I'd love to help you with that password! 🔐"
- "Nice thinking! Let me generate something super secure for you."
- "That's a great question! Here's what I'd do..."
- "Perfect! Your security is looking good!"

For VOICE/CALL MODE responses:
- Keep it EXTRA short (1 sentence max)
- Sound natural and conversational
- Use casual phrases like "Got it!", "Sure thing!", "You bet!"
- Avoid technical details unless specifically asked

Your tools: password generation, security analysis, network scanning, vulnerability checks.
Always be helpful, but keep it simple and friendly! 🚀
"""

    async def process_message(self, message: str, user_id: str, is_voice_call: bool = False) -> Dict[str, Any]:
        """
        Process a user message and return AI response with potential tool calls
        """
        try:
            # Adjust system prompt for voice call mode
            if is_voice_call:
                voice_prompt = self.system_prompt + """

VOICE CALL MODE ACTIVE:
- Keep responses to 1-2 sentences MAX
- Sound natural and conversational
- Use casual responses like "Got it!", "Sure!", "You bet!"
- Skip technical details unless critical
- Be super friendly and quick
- Perfect for natural conversation flow
"""
            else:
                voice_prompt = self.system_prompt
            
            # Add user message to conversation history
            self.conversation_history.append({
                "role": "user",
                "content": message
            })
            
            # Prepare messages for API call
            messages = [
                {"role": "system", "content": voice_prompt},
                *self.conversation_history[-10:]  # Keep last 10 messages for context
            ]
            
            # Get available tools for function calling
            tools = self.tool_manager.get_openai_tools()
            
            # Adjust parameters for voice mode
            max_tokens = 100 if is_voice_call else 500  # Shorter responses for voice
            temperature = 0.8 if is_voice_call else 0.7  # More natural for voice
            
            response = await self.client.chat.completions.create(
                model=self.settings.azure_openai_deployment_name,
                messages=messages,
                tools=tools if tools else None,
                tool_choice="auto" if tools else None,
                temperature=temperature,
                max_tokens=max_tokens
            )
            
            assistant_message = response.choices[0].message
            
            # Handle tool calls if present
            tool_results = []
            if assistant_message.tool_calls:
                for tool_call in assistant_message.tool_calls:
                    tool_result = await self.tool_manager.execute_tool(
                        tool_call.function.name,
                        json.loads(tool_call.function.arguments),
                        user_id
                    )
                    tool_results.append({
                        "tool_name": tool_call.function.name,
                        "result": tool_result
                    })
                    
                    # Add tool result to conversation for follow-up
                    self.conversation_history.append({
                        "role": "tool",
                        "content": f"Tool {tool_call.function.name} executed: {tool_result}",
                        "tool_call_id": tool_call.id
                    })
            
            # Add assistant response to history
            self.conversation_history.append({
                "role": "assistant",
                "content": assistant_message.content or ""
            })
            
            return {
                "response": assistant_message.content or "",
                "tool_calls": tool_results,
                "conversation_id": len(self.conversation_history)
            }
            
        except Exception as e:
            logger.error(f"Error processing message: {str(e)}")
            return {
                "response": "I apologize, but I encountered an error processing your request. Please try again.",
                "tool_calls": [],
                "error": str(e)
            }
    
    async def get_cybersecurity_advice(self, topic: str) -> str:
        """
        Get specific cybersecurity advice on a topic
        """
        prompt = f"""
        Provide comprehensive cybersecurity advice about: {topic}
        
        Include:
        1. Key security considerations
        2. Best practices
        3. Common vulnerabilities to avoid
        4. Recommended tools or techniques
        5. Real-world examples if applicable
        
        Keep the explanation accessible but thorough.
        """
        
        try:
            response = await self.client.chat.completions.create(
                model=self.settings.azure_openai_deployment_name,
                messages=[
                    {"role": "system", "content": self.system_prompt},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,
                max_tokens=800
            )
            
            return response.choices[0].message.content or "Unable to provide advice at this time."
            
        except Exception as e:
            logger.error(f"Error getting cybersecurity advice: {str(e)}")
            return "I apologize, but I'm unable to provide advice on that topic right now."
    
    def clear_conversation(self):
        """Clear conversation history"""
        self.conversation_history = []
    
    def get_conversation_summary(self) -> str:
        """Get a summary of the current conversation"""
        if not self.conversation_history:
            return "No conversation history."
        
        return f"Conversation with {len(self.conversation_history)} messages"
