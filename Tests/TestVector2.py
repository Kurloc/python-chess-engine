import unittest

from ChessEngine.Pathfinding.Vector2 import Vector2

from typing import List
from typing import Any
from dataclasses import dataclass
import json

from ChessEngine.Pydantic.TupleToString import tuple_to_string


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
        _data = [TweetData.from_dict(y) for y in obj.get("data")]
        _meta = Meta.from_dict(obj.get("meta"))
        return UserTweets(_data, _meta)


def test_parse(self):
    data = {
        'edit_history_tweet_ids': ['1603129273564266496'],
        'public_metrics': {
            'retweet_count': 0, 'reply_count': 0, 'like_count': 0, 'quote_count': 1
        },
        'author_id': '1516850014605266947',
        'text': '#Flowcarbon #flow3rs #Giveaway  https://t.co/pvKUolH39j @GranaryFinance @p12 @rubicondefi',
        'id': '1603129273564266496',
        'created_at': '2022-12-14T20:46:18.000Z'
    }

    z = TweetData.from_dict(data)
    print(z)

class TestVector2(unittest.TestCase):
    def test_addition(self):
        test_vector2 = Vector2.Up() + Vector2.Up()
        self.assertEqual(test_vector2.y, 2)

    def test_multiplication(self):
        test_vector2 = Vector2.Up() * 5
        self.assertEqual(test_vector2.x, 0)
        self.assertEqual(test_vector2.y, 5)

    def test(self):
        t = (0, 1)
        z = tuple_to_string(t)
        assert z == '(0, 1)'

    def test_parse(self):
        data = {
            'edit_history_tweet_ids': ['1603129273564266496'],
            'public_metrics': {
                'retweet_count': 0, 'reply_count': 0, 'like_count': 0, 'quote_count': 1
            },
            'author_id': '1516850014605266947',
            'text': '#Flowcarbon #flow3rs #Giveaway  https://t.co/pvKUolH39j @GranaryFinance @p12 @rubicondefi',
            'id': '1603129273564266496',
            'created_at': '2022-12-14T20:46:18.000Z'
        }

        z = TweetData.from_dict(data)
        print(z)


if __name__ == '__main__':
    unittest.main()
