import os
import argparse
import datetime

from libs.twitter import (
    authorize,
    search_tweets_with_query,
    search_tweets_from_user,
    format_tweet_data,
)
from libs.notify import notify_in_slack, notify_in_line
from setting import KEYWORDS, USERS, BLOCK_LIST


def get_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--consumer_key", type=str, default=None)
    parser.add_argument("--consumer_secret", type=str, default=None)
    parser.add_argument("--access_token", type=str, default=None)
    parser.add_argument("--access_secret", type=str, default=None)
    parser.add_argument("--slack_incoming_webhook_url", type=str, default=None)
    parser.add_argument("--line_token", type=str, default=None)

    return parser.parse_args()


def main() -> None:
    args = get_arguments()

    api = authorize(
        consumer_key=args.consumer_key,
        consumer_secret=args.consumer_secret,
        access_token=args.access_token,
        access_secret=args.access_secret,
    )

    # GitHub Actionsの実行時間に若干のブレがあるため，
    # 余裕を見て，実行時間の1日+30分前のツイートを対象
    now = datetime.datetime.now(tz=datetime.timezone.utc)
    start_datetime = now - datetime.timedelta(days=1, minutes=30)
    start_datetime_str = start_datetime.strftime("%Y-%m-%d_%H:%M:%S_UTC")

    tweet_data = []
    for keyword in KEYWORDS:
        tweet_data += search_tweets_with_query(
            api, keyword, start_datetime_str, BLOCK_LIST
        )

    for user in USERS:
        tweet_data += search_tweets_from_user(api, user, start_datetime)

    # 通知用のメッセージに整形
    text_list = format_tweet_data(tweet_data)

    # lineに通知
    line_token = os.getenv("LINE_TOKEN") or args.line_token
    if line_token is not None:
        notify_in_line(line_token, text_list)

    # slackに通知
    slack_incoming_webhook_url = (
        os.getenv("SLACK_INCOMING_WEBHOOK_URL") or args.slack_incoming_webhook_url
    )
    if slack_incoming_webhook_url is not None:
        notify_in_slack(slack_incoming_webhook_url, text_list)


if __name__ == "__main__":
    main()
