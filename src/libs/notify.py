from typing import List
import requests
import slackweb


LINE_NOTIFY_API = "https://notify-api.line.me/api/notify"


def notify_in_slack(slack_incoming_webhook_url: str, text_list: List[str]) -> None:
    slack_bot = slackweb.Slack(url=slack_incoming_webhook_url)
    for text in text_list:
        slack_bot.notify(text=text + "\n" + "-" * 50)


def notify_in_line(line_token: str, text_list: List[str]) -> None:
    headers = {"Authorization": f"Bearer {line_token}"}
    for text in text_list:
        data = {"message": text}
        requests.post(LINE_NOTIFY_API, headers=headers, data=data)
