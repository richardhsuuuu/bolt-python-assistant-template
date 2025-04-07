import os
import logging
import time
import json

from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
from slack_bolt.adapter.aws_lambda import SlackRequestHandler

from listeners import register_listeners

# Initialization
logging.basicConfig(level=logging.DEBUG)
app = App(process_before_response=True, ignoring_self_assistant_message_events_enabled=False)

# Register Listeners
register_listeners(app)

@app.middleware  # or app.use(log_request)
def log_request(logger, body, next):
    logger.debug(body)
    return next()

SlackRequestHandler.clear_all_log_handlers()
logging.basicConfig(format="%(asctime)s %(message)s", level=logging.DEBUG)

def handler(event, context):
    # Log received message
    logger = logging.getLogger(__name__)
    try:
        logger.info(f"Received event in handler: {json.dumps(event)}")
    except Exception as e:
        logger.error(f"Error logging event: {e}")
    
    slack_handler = SlackRequestHandler(app=app)
    return slack_handler.handle(event, context)

# Start Bolt app
if __name__ == "__main__":
    SocketModeHandler(app, os.environ.get("SLACK_APP_TOKEN")).start() 