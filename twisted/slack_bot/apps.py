import os

from django.apps import AppConfig


class SlackBotConfig(AppConfig):
    name = 'slack_bot'

    def ready(self):
        super().ready()

        if os.getenv("SLACK_MODE", "https").strip().lower() != "socket":
            return

        from .slack import slack_bot

        slack_bot.start()
