import os
import unittest
from unittest.mock import patch, Mock
import json

from python.aws_utils import (
    get_dynamo_client,
    add_item_to_table,
    get_dynamodb_resource,
    get_data_from_body,
    create_response,
)


class TestAWSUtils(unittest.TestCase):

    @patch('boto3.client')
    def test_get_dynamo_client_offline(self, mock_boto3_client):
        os.environ['IS_OFFLINE'] = 'true'
        get_dynamo_client()
        mock_boto3_client.assert_called_with('dynamodb', endpoint_url='http://localhost:8000')
        del os.environ['IS_OFFLINE']

    @patch('boto3.client')
    def test_get_dynamo_client_online(self, mock_boto3_client):
        os.environ.pop('IS_OFFLINE', None)
        get_dynamo_client()
        mock_boto3_client.assert_called_with('dynamodb')

    @patch('boto3.resource')
    def test_get_dynamodb_resource_offline(self, mock_boto3_resource):
        os.environ['IS_OFFLINE'] = 'true'
        get_dynamodb_resource()
        mock_boto3_resource.assert_called_with('dynamodb', region_name='localhost',
                                               endpoint_url='http://localhost:8000')
        del os.environ['IS_OFFLINE']

    @patch('boto3.resource')
    def test_get_dynamodb_resource_online(self, mock_boto3_resource):
        os.environ.pop('IS_OFFLINE', None)
        get_dynamodb_resource()
        mock_boto3_resource.assert_called_with('dynamodb')

    def test_get_data_from_body_with_base64(self):
        event = {
            "body": "eyJpZCI6MjMsInVzZXJuYW1lIjoidGVzdCIsInBhc3N3b3JkIjoiYmFzZTY0In0=",
            "isBase64Encoded": True
        }
        expected_data = {"id": 23, "username": "test", "password": "base64"}
        data = get_data_from_body(event)
        self.assertEqual(data, expected_data)

    def test_get_data_from_body_without_base64(self):
        event = {
            "body": {"id": 23, "username": "test", "password": "plaintext"}
        }
        expected_data = {"id": 23, "username": "test", "password": "plaintext"}
        data = get_data_from_body(event)
        self.assertEqual(data, expected_data)

    def test_create_response(self):
        expected_response = {
            "statusCode": 200,
            "headers": {
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Headers": "Content-Type",
                "Access-Control-Allow-Methods": "OPTIONS,POST",
                "Access-Control-Allow-Credentials": True,
            },
            "body": json.dumps({"message": "Test message"})
        }
        response = create_response("Test message", 200)
        self.assertEqual(response, expected_response)

    @patch('aws_utils.boto3.client')
    def test_add_item_to_table(self, mock_boto3_client):
        mock_client = Mock()
        mock_boto3_client.return_value = mock_client

        table = 'YourTableName'
        item = {"key": "value"}

        add_item_to_table(mock_client, table, item)

        mock_client.put_item.assert_called_once_with(TableName=table, Item=item)


if __name__ == '__main__':
    unittest.main()
