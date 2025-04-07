from slack_bolt import App
import logging
from .llm_caller import call_llm
import asyncio

logger = logging.getLogger(__name__)

def register_events(app: App):
    """Register all event listeners"""
    
    # Handle message events
    @app.event("message")
    def handle_message_events(body, say, logger):
        """Handle message events"""
        try:
            # Get user message
            user_message = body["event"]["text"]
            logger.info(f"Received message: {user_message}")
            
            # Get bot user ID to prevent responding to own messages
            if "bot_id" in body["event"]:
                return  # Don't respond to bot messages
            
            # Call LLM with message
            messages = [{"role": "user", "content": user_message}]
            say("right before llm!")
            response = asyncio.run(call_llm(messages))
            say("right after llm!")
            # Send response
            say(response.response)
            
        except Exception as e:
            logger.error(f"Error handling message: {e}")
            say("Sorry, I encountered an error processing your request.")
    
    # Handle app_mention events
    @app.event("app_mention")
    async def handle_mention_events(body, say, logger):
        """Handle app mention events"""
        try:
            # Get user message
            user_message = body["event"]["text"]
            logger.info(f"Received app mention: {user_message}")
            
            # Call LLM with message
            messages = [{"role": "user", "content": user_message}]
            response = await call_llm(messages)
            
            # Send response
            await say(response)
            
        except Exception as e:
            logger.error(f"Error handling app mention: {e}")
            await say("Sorry, I encountered an error processing your request.")