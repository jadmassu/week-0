import unittest
import pandas as pd
import json
from src.loader import SlackDataLoader

class SlackParserTest(unittest.TestCase):
    def setUp(self):
        self.parser = SlackDataLoader()

    def test_slack_parser(self):
        path_channel = '/path/to/json/files/'

        expected_columns = [
            'msg_type', 'user', 'msg_content', 'sender_name', 'msg_sent_time',
            'msg_dist_type', 'time_thread_start', 'reply_count',
            'reply_users_count', 'reply_users', 'tm_thread_end', 'channel'
        ]

        expected_data = [
            ['type1', 'user1', 'content1', 'sender1', 'time1', 'dist1', 'thread_start1',
             'reply_count1', 'users_count1', 'users1', 'thread_end1', 'channel_name'],
            ['type2', 'user2', 'content2', 'sender2', 'time2', 'dist2', 'thread_start2',
             'reply_count2', 'users_count2', 'users2', 'thread_end2', 'channel_name']
        ]

        expected_df = pd.DataFrame(data=expected_data, columns=expected_columns)

        actual_df = self.parser.slack_parser(path_channel)

        self.assertIsInstance(actual_df, pd.DataFrame)
        self.assertEqual(len(actual_df), len(expected_df))
        pd.testing.assert_frame_equal(actual_df, expected_df)

if __name__ == '__main__':
    unittest.main()