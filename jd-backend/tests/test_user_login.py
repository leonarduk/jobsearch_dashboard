import unittest
from unittest.mock import patch, Mock
from datetime import datetime, timedelta
import json

from user_login import login, generate_session_id, get_expiration_time

class TestUserLogin(unittest.TestCase):

    @patch('user_login.get_dynamo_client')
    @patch('user_login.generate_session_id')
    @patch('user_login.get_expiration_time')
    def test_login_successful(self, mock_get_expiration_time, mock_generate_session_id, mock_get_dynamo_client):
        mock_dynamodb_client = Mock()
        mock_get_dynamo_client.return_value = mock_dynamodb_client

        mock_generate_session_id.return_value = 'mock_session_id'
        mock_get_expiration_time.return_value = 'mock_expiration_time'

        event = {
            "body": json.dumps({"username": "test", "password": "password"})
        }

        response = login(event, None)

        mock_dynamodb_client.put_item.assert_called_once()

        expected_response = {
            "statusCode": 200,
            "body": json.dumps({
                "session_id": "mock_session_id",
                "user_name": "test"
            })
        }
        self.assertEqual(response, expected_response)


    @patch('user_login.secrets.token_hex')
    def test_generate_session_id(self, mock_token_hex):
        mock_token_hex.return_value = 'mock_session_id'

        session_id = generate_session_id()

        self.assertEqual(session_id, 'mock_session_id')


    def test_get_expiration_time(self):
        current_time = datetime(2023, 7, 22, 12, 0, 0)
        expected_expiration_time = current_time + timedelta(minutes=15)

        with patch('user_login.datetime') as mock_datetime:
            mock_datetime.utcnow.return_value = current_time

            expiration_time = get_expiration_time()

            self.assertEqual(expiration_time, expected_expiration_time.strftime('%Y-%m-%dT%H:%M:%SZ'))

    @patch('user_login.get_dynamo_client')
    @patch('user_login.generate_session_id')
    @patch('user_login.get_expiration_time')
    def test_login_successful(self, mock_get_expiration_time, mock_generate_session_id, mock_get_dynamo_client):
        mock_dynamodb_client = Mock()
        mock_get_dynamo_client.return_value = mock_dynamodb_client

        mock_generate_session_id.return_value = 'mock_session_id'
        mock_get_expiration_time.return_value = 'mock_expiration_time'

        event = {
            "body": json.dumps({"username": "test", "password": "password"})
        }

        response = login(event, None)

        mock_dynamodb_client.put_item.assert_called_once()

        expected_response = {
            "statusCode": 200,
            "body": json.dumps({
                "session_id": "mock_session_id",
                "user_name": "test"
            })
        }
        self.assertEqual(response, expected_response)



if __name__ == '__main__':
    unittest.main()
