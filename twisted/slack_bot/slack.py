import os
from typing import Any

from slack_sdk import WebClient


class SlackBot:
	def __init__(self, token: str | None = None, cc_group_id: str | None = None):
		slack_token = token
		self.client = WebClient(token=slack_token)
		self._cc_group_id = cc_group_id

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
	def error_log(
		self,
		*,
		channel: str,
		error: str,
		title: str | None = None,
		**kwargs: Any,
	):
		if title is None:
			title = "Error Log"

		group_id = self._cc_group_id
		mention = f"<@{group_id}>" if group_id else ""

		# Parent message
		parent = self.client.chat_postMessage(
			channel=channel,
			text=f"{title}".strip(),
			blocks=[
				{
					"type": "section",
					"text": {
						"type": "mrkdwn",
						"text": f"*{title}*".strip(),
					},
				},
			],
		)

		# Thread message
		thread_text = f"```{error}```"
		if mention:
			thread_text += f"\n\nCC: {mention}"

		return self.client.chat_postMessage(
			channel=channel,
			thread_ts=parent["ts"],
			text=thread_text,
			blocks=[
				{
					"type": "section",
					"text": {
						"type": "mrkdwn",
						"text": thread_text,
					},
				},
			],
		)

	def users_info(self, *, user: str):
		return self.client.users_info(user=user)


slack_token = os.getenv("SLACK_TOKEN")
cc_group_id = os.getenv("SLACK_CC_GROUP_ID")

slack_bot = SlackBot(token=slack_token, cc_group_id=cc_group_id)
slack_client = slack_bot.client
