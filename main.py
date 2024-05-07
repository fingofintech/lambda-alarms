import requests
import json
import os

from dotenv import load_dotenv

load_dotenv()


def handler(event=None, context=None):
    webhook_url = os.getenv('SLACK_WEBHOOK_URL')
    alarm_name = event['detail']['alarmName']
    new_state = event['detail']['state']['value']
    old_state = event['detail']['previousState']['value']
    reason = event['detail']['state']['reason']
    emoji_state = lambda state: ":white_check_mark:" if state == "OK" else ":x:"
    slack_users_dev = "<!subteam^S06HBEQB8ES>" # @dev in slack

    slack_message = {
        "blocks": [
            {
                "type": "header",
                "text": {
                    "type": "plain_text",
                    "text": f"{emoji_state(new_state)} Alarma Activada: {alarm_name} {emoji_state(new_state)}",
                    "emoji": True
                }
            },
            {
                "type": "section",
                "fields": [
                    {
                        "type": "mrkdwn",
                        "text": f"*Estado Anterior:*\n{emoji_state(old_state)}"
                    },
                    {
                        "type": "mrkdwn",
                        "text": f"*Estado Nuevo:*\n{emoji_state(new_state)}"
                    }
                ]
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"*Razón del Cambio:*\n{reason}"
                }
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"{slack_users_dev}"
                }
            },
            {
                "type": "context",
                "elements": [
                    {
                        "type": "mrkdwn",
                        "text": f"Actualizado el: {event['time']}"
                    }
                ]
            }
        ]
    }
    
    response = requests.post(
        webhook_url, data=json.dumps(slack_message),
        headers={'Content-Type': 'application/json'}
    )
    return response.text
