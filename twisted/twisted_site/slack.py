import os
from typing import Any
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler


class SlackBot:
	def __init__(
		self,
		token: str | None = None,
		signing_secret: str | None = None,
		cc_group_id: str | None = None,
		app_token: str | None = None,
		slack_mode: str | None = None,
	):
		self.slack_mode = (slack_mode or os.getenv("SLACK_MODE", "https")).lower()
		self.app_token = app_token or os.getenv("SLACK_APP_TOKEN")
		slack_token = token
		self.app = App(token=slack_token, signing_secret=signing_secret)
		self.socket_mode_handler: SocketModeHandler | None = None
		if self.slack_mode == "socket":
			if not self.app_token:
				raise ValueError("SLACK_APP_TOKEN must be set when SLACK_MODE=socket")
			self.socket_mode_handler = SocketModeHandler(self.app, self.app_token)
		self.client = self.app.client
		self._cc_group_id = cc_group_id

	def start(self):
		if self.socket_mode_handler is not None:
			self.socket_mode_handler.start()

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
slack_signing_secret = os.getenv("SLACK_SIGNING_SECRET")
cc_group_id = os.getenv("SLACK_CC_GROUP_ID")
slack_mode = os.getenv("SLACK_MODE", "https").strip().lower()
slack_app_token = os.getenv("SLACK_APP_TOKEN")

slack_bot = SlackBot(
	token=slack_token,
	signing_secret=slack_signing_secret,
	cc_group_id=cc_group_id,
	app_token=slack_app_token,
	slack_mode=slack_mode,
)
slack_client = slack_bot.client