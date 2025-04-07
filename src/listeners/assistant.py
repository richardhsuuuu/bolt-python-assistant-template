import logging
from typing import List, Dict
from slack_bolt import Assistant, BoltContext, Say, SetSuggestedPrompts, SetStatus
from slack_bolt.context.get_thread_context import GetThreadContext
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
import asyncio
from .llm_caller import call_llm

# Refer to https://tools.slack.dev/bolt-python/concepts/assistant/ for more details
assistant = Assistant()


# This listener is invoked when a human user opened an assistant thread
@assistant.thread_started
def start_assistant_thread(
    say: Say,
    get_thread_context: GetThreadContext,
    set_suggested_prompts: SetSuggestedPrompts,
    logger: logging.Logger,
):
    try:
        say("How can I help you?")

        prompts: List[Dict[str, str]] = [
            {
                "title": "AI Alignment",
                "message": "What are the key challenges in aligning advanced AI systems with human values and intentions?",
            },
            {
                "title": "Macro Investing",
                "message": "What are the key principles and strategies that only top-tier hedge fund investors like Tiger Global use to navigate global markets?",
            },
            {
                "title": "AI Explainability",
                "message": "What are the current limitations and future prospects for making complex AI systems more interpretable and explainable?",
            },
        ]

        thread_context = get_thread_context()
        if thread_context is not None and thread_context.channel_id is not None:
            summarize_channel = {
                "title": "Summarize the referred channel",
                "message": "Can you generate a brief summary of the referred channel?",
            }
            prompts.append(summarize_channel)

        set_suggested_prompts(prompts=prompts)
    except Exception as e:
        logger.exception(f"Failed to handle an assistant_thread_started event: {e}", e)
        say(f":warning: Something went wrong! ({e})")


# This listener is invoked when the human user sends a reply in the assistant thread
@assistant.user_message
def respond_in_assistant_thread(
    payload: dict,
    logger: logging.Logger,
    context: BoltContext,
    set_status: SetStatus,
    get_thread_context: GetThreadContext,
    set_suggested_prompts: SetSuggestedPrompts,
    client: WebClient,
    say: Say,
):
    try:
        user_message = payload["text"]
        set_status("is thinking & typing...")

        if user_message == "Can you generate a brief summary of the referred channel?":
            # the logic here requires the additional bot scopes:
            # channels:join, channels:history, groups:history
            thread_context = get_thread_context()
            referred_channel_id = thread_context.get("channel_id")
            try:
                channel_history = client.conversations_history(channel=referred_channel_id, limit=50)
            except SlackApiError as e:
                if e.response["error"] == "not_in_channel":
                    # If this app's bot user is not in the public channel,
                    # we'll try joining the channel and then calling the same API again
                    client.conversations_join(channel=referred_channel_id)
                    channel_history = client.conversations_history(channel=referred_channel_id, limit=50)
                else:
                    raise e

            prompt = f"Can you generate a brief summary of these messages in a Slack channel <#{referred_channel_id}>?\n\n"
            for message in reversed(channel_history.get("messages")):
                if message.get("user") is not None:
                    prompt += f"\n<@{message['user']}> says: {message['text']}\n"
            messages_in_thread = [{"role": "user", "content": prompt}]
            returned_message = asyncio.run(call_llm(messages_in_thread))
            say(returned_message)
            return

        replies = client.conversations_replies(
            channel=context.channel_id,
            ts=context.thread_ts,
            oldest=context.thread_ts,
            limit=10,
        )
        messages_in_thread: List[Dict[str, str]] = []
        for message in replies["messages"]:
            role = "user" if message.get("bot_id") is None else "assistant"
            messages_in_thread.append({"role": role, "content": message["text"]})
        chat_output = asyncio.run(call_llm(messages_in_thread))
        say(chat_output.response)

        if chat_output.follow_up_prompt_questions:
            prompts = [{"title": question, "message": question} for question in chat_output.follow_up_prompt_questions]
            set_suggested_prompts(prompts=prompts[:3] if len(prompts) > 3 else prompts)


    except Exception as e:
        logger.exception(f"Failed to handle a user message event: {e}")
        say(f":warning: Something went wrong! ({e})")