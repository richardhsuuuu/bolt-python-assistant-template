from slack_bolt import App
import logging
import time
from .llm_caller import call_llm
import asyncio

logger = logging.getLogger(__name__)

def register_commands(app: App):
    """Register all command listeners"""
    
    # Handle /ask command
    @app.command("/ask")
    async def handle_ask_command(ack, command, respond):
        """Handle /ask command"""
        # Acknowledge command request
        await ack()
        
        try:
            # Get user query
            user_query = command["text"]
            logger.info(f"Received /ask command: {user_query}")
            
            if not user_query.strip():
                await respond("Please provide a question or prompt with the /ask command.")
                return
            
            # Process with LLM
            messages = [{"role": "user", "content": user_query}]
            response = await call_llm(messages)
            
            # Respond
            await respond(response)
            
        except Exception as e:
            logger.error(f"Error handling /ask command: {e}")
            await respond("Sorry, I encountered an error processing your request.")

    # Handle /hello-bolt-python-lambda command
    @app.command("/hello-bolt-python-lambda")
    def handle_hello_command(ack, body, logger):
        """Handle /hello-bolt-python-lambda command"""
        logger.info(f"Received hello command: {body}")
        
        if body.get("text") is None:
            ack(f":x: Usage: /hello-bolt-python-lambda (description here)")
        else:
            title = body["text"]
            ack(f"Accepted! (task: {title})")
            
            # Process the request asynchronously
            def process_request():
                time.sleep(5)
                title = body["text"]
                return f"Completed! (task: {title})"
            
            # Return the process_request function to be executed lazily
            return process_request 