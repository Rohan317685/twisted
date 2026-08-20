from slack_bolt.adapter.django import SlackRequestHandler
from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from .slack import slack_bot

# Initialize the handler
handler = SlackRequestHandler(slack_bot.app)


@csrf_exempt
def slack_events(request):
    """
    Slack events endpoint handler for:
    - App mentions and messages
    - Slash commands
    - Shortcuts
    - Interactive components
    """
    return handler.handle(request)


# ==================== Event Handlers ====================


@slack_bot.app.event("app_mention")
def handle_app_mention(body, say, logger):
    """Handle when the bot is mentioned in a message"""
    logger.debug(f"App mention event: {body}")
    say(f"Thanks for the mention! <@{body['event']['user']}>")


@slack_bot.app.event("message")
def handle_message(body, logger):
    """Handle regular messages (optional, remove if not needed)"""
    logger.debug(f"Message event: {body}")


# ==================== Slash Commands ====================


# @slack_bot.app.command("/hellotwisted")
# def handle_hello_command(ack, respond, command):
#     """
#     Slash command: /hellotwisted
#     Responds with a greeting and user information
#     """
#     ack()
#     respond(
#         text=f"Hello <@{command['user_id']}>! 👋",
#         blocks=[
#             {
#                 "type": "section",
#                 "text": {
#                     "type": "mrkdwn",
#                     "text": f"Hello <@{command['user_id']}> from the Twisted Slack Bot! 👋",
#                 },
#             },
#             {
#                 "type": "section",
#                 "fields": [
#                     {"type": "mrkdwn", "text": f"*User:*\n<@{command['user_id']}>"},
#                     {"type": "mrkdwn", "text": f"*Channel:*\n<#{command['channel_id']}>"},
#                 ],
#             },
#         ],
#     )


def ack_short_handler(ack):
    ack()

def hellotwistedcommand(respond, body):
    user = body["user"]["id"]
    respond(text=f"Hello <@{user}> from the Twisted Slack Bot! 👋")

slack_bot.app.command("/hellotwisted")(
    ack=ack_short_handler,
    lazy=[hellotwistedcommand]
)
