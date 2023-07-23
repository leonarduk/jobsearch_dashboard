import json
import bcrypt
import boto3

dynamodb = boto3.resource('dynamodb')
user_table = dynamodb.Table('JD_User')


def signup(event, context):
    data = json.loads(event['body'])

    # Validate input
    name = data.get('name')
    email = data.get('email')
    password = data.get('password')

    if not name or not email or not password:
        response = {
            "statusCode": 400,
            "body": json.dumps({"message": "Name, email, and password are required."})
        }
        return response

    # Check if user already exists
    response = user_table.get_item(Key={'email': email})
    if 'Item' in response:
        response = {
            "statusCode": 409,
            "body": json.dumps({"message": "User with this email already exists."})
        }
        return response

    # Hash the password
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    # Save user record in the database
    user_table.put_item(Item={'email': email, 'name': name, 'password': hashed_password})

    # Return response
    response = {
        "statusCode": 200,
        "body": json.dumps({"message": "User created successfully."})
    }
    return response
