from slack_bolt import App
import logging

# Import all listeners
from .events import register_events
from .commands import register_commands
from .assistant import assistant


logger = logging.getLogger(__name__)

def register_listeners(app: App):
    """Register all listeners with the app"""
    logger.info("Registering all listeners")
    
    # Register different types of listeners
    app.assistant(assistant)
    register_events(app)
    register_commands(app)
    
    logger.info("All listeners registered") 