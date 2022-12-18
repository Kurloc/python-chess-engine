import json
import unittest

from dataclasses import dataclass
from typing import List, Dict

import requests as requests


@dataclass
class TweetData:
    id: str
    edit_history_tweet_ids: list[str]
    text: str
    author_id: str
    created_at: str
    retweet_count: int
    reply_count: int
    like_count: int
    quote_count: int

    @staticmethod
    def from_dict(obj: any) -> 'TweetData':
        _id = str(obj.get("id"))
        edit_history_tweet_ids = [y for y in obj.get("edit_history_tweet_ids")]
        text = str(obj.get("text"))
        author_id = str(obj.get("author_id"))
        created_at = str(obj.get("created_at"))
        public_metrics = obj.get("public_metrics", {})
        retweet_count = public_metrics.get("retweet_count", 0)
        reply_count = public_metrics.get("reply_count", 0)
        like_count = public_metrics.get("like_count", 0)
        quote_count = public_metrics.get("quote_count", 0)

        return TweetData(_id, edit_history_tweet_ids, text, author_id, created_at, retweet_count, reply_count,
                         like_count, quote_count)


@dataclass
class Meta:
    next_token: str
    result_count: int
    newest_id: str
    oldest_id: str

    @staticmethod
    def from_dict(obj: any) -> 'Meta':
        _next_token = str(obj.get("next_token"))
        _result_count = int(obj.get("result_count"))
        _newest_id = str(obj.get("newest_id"))
        _oldest_id = str(obj.get("oldest_id"))
        return Meta(_next_token, _result_count, _newest_id, _oldest_id)


@dataclass
class UserTweets:
    data: list[TweetData]
    meta: Meta

    @staticmethod
    def from_dict(obj: any) -> 'UserTweets':
        try:
            _data = [TweetData.from_dict(y) for y in obj.get("data")]
            _meta = Meta.from_dict(obj.get("meta"))
            return UserTweets(_data, _meta)
        except Exception as e:
            print(e)
            print(obj)
            return None


@dataclass
class AllTweets:
    tweet_pages: List[UserTweets]

    def add_tweets(self, incoming_dict_value: Dict) -> None:
        _tweet_pages = UserTweets.from_dict(incoming_dict_value)
        self.tweet_pages.append(_tweet_pages)


class TestParse(unittest.TestCase):

    def test_get_all_user_tweet_pages_combined(self) -> List[TweetData]:
        all_tweets = []
        user_tweets = UserTweets.from_dict(self.get_user_tweets())
        all_tweets.extend(user_tweets.data)

        while user_tweets.meta.next_token != 'None' and user_tweets.meta.next_token is not None:
            user_tweets = UserTweets.from_dict(
                self.get_user_tweets(
                    user_tweets.meta.next_token
                )
            )
            all_tweets.extend(user_tweets.data)

        return all_tweets

    @staticmethod
    def get_user_tweets(pagination_token=None) -> Dict:
        bearer_token = "AAAAAAAAAAAAAAAAAAAAAI55jgEAAAAAx2XbqTphUHttys43DnSnjg8KgZ8%3DD3IQaCGJ1M68QUWeAwK8FJf6Cc2azEfKQ4OQaCYn7nFYap53wZ"
        pagination_token = '' if pagination_token is None else f'&pagination_token={pagination_token}'
        time_line_query_params = f'max_results=100&tweet.fields=created_at,public_metrics,author_id{pagination_token}'
        time_line = json.loads(
            requests.get(
                f'https://api.twitter.com/2/users/1280325738537914374/tweets?{time_line_query_params}',
                headers={
                    "Authorization": f"Bearer {bearer_token}",
                    "User-Agent": "v2UserTweetsPython"
                }
            ).content.decode('utf-8')
        )
        return time_line

    def test(self):
        all_tweets = []
        bearer_token = "AAAAAAAAAAAAAAAAAAAAAI55jgEAAAAAx2XbqTphUHttys43DnSnjg8KgZ8%3DD3IQaCGJ1M68QUWeAwK8FJf6Cc2azEfKQ4OQaCYn7nFYap53wZ"
        user_tweets = UserTweets.from_dict(
            json.loads(
                requests.get(
                    'https://api.twitter.com/2/users/1280325738537914374/tweets?max_results=100&tweet.fields=created_at,public_metrics,author_id',
                    headers={"Authorization": f"Bearer {bearer_token}", "User-Agent": "v2UserTweetsPython"}
                ).content.decode('utf-8')
            )
        )
        all_tweets.extend(user_tweets.data)
        while user_tweets.meta.next_token is not None and user_tweets.meta.next_token != 'None':
            print('new page')
            user_tweets = UserTweets.from_dict(
                json.loads(
                    requests.get(
                        'https://api.twitter.com/2/users/1280325738537914374/tweets?max_results=100&tweet.fields=created_at,public_metrics,author_id&pagination_token=' +
                        user_tweets.meta.next_token,
                        headers={"Authorization": f"Bearer {bearer_token}", "User-Agent": "v2UserTweetsPython"}
                    ).content.decode('utf-8')
                )
            )
            all_tweets.extend(user_tweets.data)
        print(all_tweets)


if __name__ == '__main__':
    unittest.main()
