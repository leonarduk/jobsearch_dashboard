import unittest
from unittest.mock import patch, Mock

# Import the functions to be tested
from aws_utils import (
    create_response,
)
from user_signup import signup


class TestUserSignup(unittest.TestCase):

    @patch('user_signup.get_data_from_body')
    @patch('user_signup.get_dynamo_client')
    @patch('user_signup.add_item_to_table')
    def test_successful_signup(self, mock_add_item, mock_get_dynamo_client, mock_get_data_from_body):
        # Set up mock objects
        mock_data = {
            'name': 'John Doe',
            'email': 'john@example.com',
            'password': 'testpassword',
        }
        mock_get_data_from_body.return_value = mock_data
        mock_dynamodb_client = Mock()
        mock_get_dynamo_client.return_value = mock_dynamodb_client

        # Mock DynamoDB get_item response to indicate user does not exist
        mock_dynamodb_client.get_item.return_value = {}

        # Run the signup function
        result = signup(event={}, context={})

        # Check if the expected responses were called
        mock_get_data_from_body.assert_called_once()
        mock_get_dynamo_client.assert_called_once()
        mock_dynamodb_client.get_item.assert_called_once_with(
            TableName='JD_User',
            Key={'UserId': {'S': 'john@example.com'}}
        )
        mock_add_item.assert_called_once_with(
            dynamodb_client=mock_dynamodb_client,
            table='JD_User',
            item={
                'UserId': {'S': 'john@example.com'},
                'Email': {'S': 'john@example.com'},
                'Name': {'S': 'John Doe'},
                'Password': {'S': 'testpassword'},
            }
        )

        # Check the response
        expected_response = create_response("User created successfully.", 200)
        self.assertEqual(result, expected_response)

    # Add more test cases for other scenarios (existing user, invalid input, etc.)


if __name__ == '__main__':
    unittest.main()
