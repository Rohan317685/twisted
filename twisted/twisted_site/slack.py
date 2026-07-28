import os
from typing import Any

from slack_sdk import WebClient


class SlackBot:
	def __init__(self, token: str | None = None):
		slack_token = token
		self.client = WebClient(token=slack_token)

	def post_message(
		self,
		*,
		channel: str,
		text: str,
		blocks: list[dict[str, Any]] | None = None,
		**kwargs: Any,
	):
		payload: dict[str, Any] = {
			"channel": channel,
			"text": text,
			**kwargs,
		}
		if blocks is not None:
			payload["blocks"] = blocks
		return self.client.chat_postMessage(**payload)

	def send_message(self, *, channel: str, text: str, **kwargs: Any):
		return self.post_message(channel=channel, text=text, **kwargs)

	def send_blocks(
		self,
		*,
		channel: str,
		blocks: list[dict[str, Any]],
		text: str = " ",
		**kwargs: Any,
	):
		return self.post_message(channel=channel, text=text, blocks=blocks, **kwargs)

	def users_info(self, *, user: str):
		return self.client.users_info(user=user)


slack_bot = SlackBot(token=os.environ["SLACK_TOKEN"])
slack_client = slack_bot.client
