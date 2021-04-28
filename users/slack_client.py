from django.conf import settings
from slack_sdk.web import WebClient


def send_slack_message(message, channel):
    slack_web_client = WebClient(token=settings.SLACK_SDK_OAUTH_TOKEN)
    block = {
        'type': 'section',
        'text': {
            'type': 'mrkdwn',
            'text': message
        }
    }
    if channel[0] != '@':
        channel = '@' + channel
    response = slack_web_client.chat_postMessage(
        channel=channel,
        username=settings.SLACK_USERNAME,
        icon_emoji=':robot_face:',
        blocks=[block]
    )
    if not response.status_code == 200 or response.data.get('ok') is not True:
        # Here there should be code to manage errors, like logs, etc.
        pass
