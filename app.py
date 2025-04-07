# import os
# import logging
# import time

# from slack_bolt import App
# from slack_bolt.adapter.socket_mode import SocketModeHandler
# from slack_bolt.adapter.aws_lambda import SlackRequestHandler

# from listeners import register_listeners

# # Initialization
# logging.basicConfig(level=logging.DEBUG)
# # app = App(token=os.environ.get("SLACK_BOT_TOKEN"))
# app = App(process_before_response=True)

# # Register Listeners
# register_listeners(app)


# @app.middleware  # or app.use(log_request)
# def log_request(logger, body, next):
#     logger.debug(body)
#     return next()


# command = "/hello-bolt-python-lambda"


# def respond_to_slack_within_3_seconds(body, ack):
#     if body.get("text") is None:
#         ack(f":x: Usage: {command} (description here)")
#     else:
#         title = body["text"]
#         ack(f"Accepted! (task: {title})")


# def process_request(respond, body):
#     time.sleep(5)
#     title = body["text"]
#     respond(f"Completed! (task: {title})")


# app.command(command)(ack=respond_to_slack_within_3_seconds, lazy=[process_request])

# SlackRequestHandler.clear_all_log_handlers()
# logging.basicConfig(format="%(asctime)s %(message)s", level=logging.DEBUG)

# def handler(event, context):
#     slack_handler = SlackRequestHandler(app=app)
#     return slack_handler.handle(event, context)


# # Start Bolt app
# if __name__ == "__main__":
#     SocketModeHandler(app, os.environ.get("SLACK_APP_TOKEN")).start()
