import base64
import json
#import bcrypt
import chardet

import boto3

dynamodb = boto3.resource('dynamodb', region_name='localhost', endpoint_url='http://localhost:8000')

user_table = dynamodb.Table('JD_User')


def signup(event, context):
    try:
        # print("event: " + str(event))

        # Decode the base64-encoded request body
        body = event['body']
        print("body: " + str(body))

        isb64Encoded = event['isBase64Encoded']
        if isb64Encoded:
            decoded_data = base64.b64decode(body)
            # Use chardet to detect the character encoding
            result = chardet.detect(decoded_data)
            encoding = result['encoding']
            request_body = decoded_data.decode(encoding)
        else:
            request_body = body
        data = json.loads(request_body)

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

        # Check if user already exists
        response = user_table.get_item(Key={'userId': email})
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

        # Save user record in the database
        user_table.put_item(Item={'userId': email, 'email': email, 'name': name, 'password': password})

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
            "body": json.dumps({"message": "An error occurred during sign up."})
        }
        return response