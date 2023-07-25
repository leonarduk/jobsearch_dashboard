# handler.py
import json
import bcrypt
import boto3

dynamodb = boto3.resource('dynamodb')
user_table = dynamodb.Table('JD_User')
session_table = dynamodb.Table('JD_Sessions')


def login(event, context):
    data = json.loads(event['body'])
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return {
            "statusCode": 400,
            "body": json.dumps({"message": "Username and password are required."})
        }

    # Lookup user by username
    response = user_table.get_item(Key={'username': username})
    if 'Item' not in response:
        return {
            "statusCode": 401,
            "body": json.dumps({"message": "Invalid username or password."})
        }

    user = response['Item']
    stored_password_hash = user['password']

    # Validate password
    if not bcrypt.checkpw(password.encode('utf-8'), stored_password_hash.encode('utf-8')):
        return {
            "statusCode": 401,
            "body": json.dumps({"message": "Invalid username or password."})
        }

    # Generate session ID (you can use any secure random string generator)
    # In a production setting, consider using UUID or other secure session ID generators.
    session_id = generate_session_id()

    # Save session ID to the JD_Sessions table with an expiration time (e.g., 15 minutes)
    session_table.put_item(
        Item={'session_id': session_id, 'user_id': user['user_id'], 'expiration': get_expiration_time()})

    # Return the session ID to the client
    return {
        "statusCode": 200,
        "body": json.dumps({"session_id": session_id})
    }


def generate_session_id():
    # Implement your secure session ID generator logic here
    # For example, you can use secrets module to generate random strings.
    # In a production setting, consider using UUID or other secure session ID generators.
    pass


def get_expiration_time():
    # Implement your logic to calculate the expiration time for the session (e.g., 15 minutes from now).
    pass
