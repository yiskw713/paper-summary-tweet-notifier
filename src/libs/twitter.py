import os
from typing import Optional, List, Tuple, Set
import tweepy
import datetime


def authorize(
    consumer_key: Optional[str] = None,
    consumer_secret: Optional[str] = None,
    access_token: Optional[str] = None,
    access_secret: Optional[str] = None,
) -> tweepy.API:
    consumer_key = consumer_key or os.getenv("CONSUMER_KEY")
    consumer_secret = consumer_secret or os.getenv("CONSUMER_SECRET")
    access_token = access_token or os.getenv("ACCESS_TOKEN")
    access_secret = access_secret or os.getenv("ACCESS_SECRET")

    if consumer_key is None or consumer_secret is None:
        raise ValueError("Both CONSMER_KEY and CONSUMER_SECRET must be specified.")

    if access_token is None or access_secret is None:
        raise ValueError("Both ACCESS_TOKEN and ACCESS_SECRET must be specified.")

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_secret)

    api = tweepy.API(auth)
    return api


def search_tweets_with_query(
    api: tweepy.API,
    keyword: str,
    start_datetime_str: str,
    block_list: Set[str],
) -> List[Tuple[str, str, str]]:
    query = f"{keyword} since:{start_datetime_str}"

    response = []

    tweets = api.search_tweets(q=query, lang="ja", tweet_mode="extended", count=100)
    for tweet in tweets:
        # 除外したいユーザーのツイートは無視
        if tweet.user.screen_name in block_list:
            continue

        # RTは無視
        if tweet.retweeted or "RT @" in tweet.full_text:
            continue

        # username, tweet_id, textを保存
        response.append((tweet.user.screen_name, tweet.id_str, tweet.full_text))

    return response


def search_tweets_from_user(
    api: tweepy.API, user: str, start_datetime: datetime.datetime
) -> List[Tuple[str, str, str]]:
    tweets = api.user_timeline(
        screen_name=user,
        count=100,
        include_rts=True,
        tweet_mode="extended",
    )

    response = []
    for tweet in tweets:
        # tweetは新しい順に取得されているため，
        # 指定した日付以前のtweetが見つかったら，for文を終了
        if tweet.created_at < start_datetime:
            break

        # リプライは無視
        # https://github.com/tweepy/tweepy/issues/1526
        if tweet.in_reply_to_status_id is not None:
            continue

        # username, tweet_id, textを保存
        response.append((tweet.user.screen_name, tweet.id_str, tweet.full_text))

    return response


def format_tweet_data(tweet_data: List[Tuple[str, str, str]]) -> List[str]:
    response: List[str] = []
    for screen_name, id_str, full_text in tweet_data:
        url = f"https://twitter.com/{screen_name}/status/{id_str}"
        message = f"\n{full_text}\n\ntweet URL: {url}"
        response.append(message)

    return response
