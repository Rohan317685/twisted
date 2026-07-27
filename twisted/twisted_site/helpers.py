import os
import slack

slack_client = slack.WebClient(token=os.environ['SLACK_TOKEN'])