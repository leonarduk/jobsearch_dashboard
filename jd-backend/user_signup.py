import json

import boto3

from aws_utils import get_data_from_body, get_dynamodb_resource


dynamodb_resource = get_dynamodb_resource()

table_name='JD_User'

def signup(event, context):
    try:
        # print("event: " + str(event))

        data = get_data_from_body(event)

        print("Data" + str(data))

        # Validate input
        name = data.get('name')
        email = data.get('email')
        password = data.get('password')

        if not name or not email or not password:
            response = {
                "statusCode": 400,
                "headers": {
                    "Access-Control-Allow-Origin": "*",  # Allow requests from any domain
                    "Access-Control-Allow-Headers": "Content-Type",  # Add any required headers here
                    "Access-Control-Allow-Methods": "OPTIONS,POST",  # Add allowed HTTP methods here
                    "Access-Control-Allow-Credentials": True,  # Allow sending of cookies
                },
                "body": json.dumps({"message": "Name, email, and password are required."})
            }
            return response
        dynamodb = boto3.client('dynamodb', endpoint_url='http://localhost:8000')
        dynamodb.get_waiter('table_exists').wait(TableName=table_name)
        print(f"Table '{table_name}' created successfully.")

        # Check if user already exists
        user_table = dynamodb_resource.Table('JD_User')
        print(f"table {user_table}")
        # Perform the get_item operation using the client
        response = dynamodb.get_item(
            TableName=table_name,
            Key={'UserId': {'S': email}}
        )

        if 'Item' in response:
            response = {
                "statusCode": 409,
                "headers": {
                    "Access-Control-Allow-Origin": "*",  # Allow requests from any domain
                    "Access-Control-Allow-Headers": "Content-Type",  # Add any required headers here
                    "Access-Control-Allow-Methods": "OPTIONS,POST",  # Add allowed HTTP methods here
                    "Access-Control-Allow-Credentials": True,  # Allow sending of cookies
                },
                "body": json.dumps({"message": "User with this email already exists."})
            }
            return response

        # Hash the password
        #    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

        # Perform the put_item operation using the client
        response = dynamodb.put_item(
            TableName=table_name,
            Item={
                'UserId': {'S': email},
                'Email': {'S': email},
                'Name': {'S': name},
                'Password': {'S': password}
            }
        )
        # Return response
        response = {
            "statusCode": 200,
            "headers": {
                "Access-Control-Allow-Origin": "*",  # Allow requests from any domain
                "Access-Control-Allow-Headers": "Content-Type",  # Add any required headers here
                "Access-Control-Allow-Methods": "OPTIONS,POST",  # Add allowed HTTP methods here
                "Access-Control-Allow-Credentials": True,  # Allow sending of cookies
            },
            "body": json.dumps({"message": "User created successfully."})
        }

        return response

    except Exception as e:
        print("Error" + str(e))
        # Handle any exceptions and return an error response
        response = {
            "statusCode": 500,
            "headers": {
                "Access-Control-Allow-Origin": "*",  # Allow requests from any domain
                "Access-Control-Allow-Headers": "Content-Type",  # Add any required headers here
                "Access-Control-Allow-Methods": "OPTIONS,POST",  # Add allowed HTTP methods here
                "Access-Control-Allow-Credentials": True,  # Allow sending of cookies
            },
            "body": json.dumps({"message": f"An error occurred during sign up.{e}"})
        }
        return response


