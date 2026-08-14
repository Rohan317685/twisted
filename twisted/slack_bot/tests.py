from unittest.mock import Mock, patch

from django.test import SimpleTestCase

from .slack import SlackBot


class SlackBotModeTests(SimpleTestCase):
    @patch("slack_bot.slack.threading.Thread")
    @patch("slack_bot.slack.SocketModeHandler")
    def test_socket_mode_starts_in_background_thread(self, socket_handler_cls, thread_cls):
        socket_handler = Mock()
        socket_handler_cls.return_value = socket_handler
        thread_instance = Mock()
        thread_cls.return_value = thread_instance

        bot = SlackBot(
            token="xoxb-test",
            signing_secret="secret",
            app_token="xapp-test",
            slack_mode="socket",
        )

        bot.start()

        socket_handler_cls.assert_called_once_with(bot.app, "xapp-test")
        thread_cls.assert_called_once_with(
            target=socket_handler.start,
            name="slack-socket-mode",
            daemon=True,
        )
        thread_instance.start.assert_called_once_with()

    @patch("slack_bot.slack.threading.Thread")
    @patch("slack_bot.slack.SocketModeHandler")
    def test_https_mode_does_not_start_socket_thread(self, socket_handler_cls, thread_cls):
        bot = SlackBot(
            token="xoxb-test",
            signing_secret="secret",
            app_token="xapp-test",
            slack_mode="https",
        )

        bot.start()

        socket_handler_cls.assert_not_called()
        thread_cls.assert_not_called()
