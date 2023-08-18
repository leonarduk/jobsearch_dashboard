import json
import secrets
from datetime import datetime, timedelta
import logging

from python.aws_utils import get_data_from_body, get_dynamo_client, log_and_raise_error, add_item_to_table

# Initialize the logger
logger = logging.getLogger(__name__)


def login(event, context):
    data = get_data_from_body(event)

    logger.info(f"Data: {data}")

    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        log_and_raise_error("Username and password are required.", "LOGIN_VALIDATION_FAILURE")

    user_table = "JD_User"
    dynamodb_client = get_dynamo_client()
    dynamodb_client.get_waiter('table_exists').wait(TableName=user_table)

    # Check if db_user already exists
    response = dynamodb_client.get_item(
        TableName=user_table,
        Key={'UserId': {'S': username}}
    )

    if 'Item' not in response:
        log_and_raise_error("Invalid username or password.", "INVALID_CREDENTIALS")

    db_user = response['Item']
    logger.info(f"db_user {db_user}")
    stored_password_hash = db_user['Password']['S']

    # Validate password
    # if not bcrypt.checkpw(password.encode('utf-8'), stored_password_hash.encode('utf-8')):
    if stored_password_hash != password:
        log_and_raise_error("Invalid username or password.", "INVALID_CREDENTIALS")

    # Generate session ID
    session_id = generate_session_id()

    # Save session ID to the JD_Sessions table with an expiration time
    session_table = "JD_Sessions"
    dynamodb_client = get_dynamo_client()
    dynamodb_client.get_waiter('table_exists').wait(TableName=session_table)

    add_item_to_table(dynamodb_client=dynamodb_client, table=session_table,
                      item={
                          'session_id': {'S': session_id},
                          'user_id': {'S': username},
                          'expiration': {'S': get_expiration_time()}})

    # Return the session ID to the client
    logger.info(f"User {username} logged in with session ID: {session_id}")
    return {
        "statusCode": 200,
        "body": json.dumps({
            "session_id": session_id,
            "user_name": username  # Replace this with the actual variable containing the user's name
        })
    }


def generate_session_id():
    # Generate a secure random session ID using the secrets module
    # In a production setting, consider using UUID or other secure session ID generators.
    return secrets.token_hex(16)  # Generate a random 32-character hexadecimal string


def get_expiration_time():
    # Calculate the current time
    current_time = datetime.utcnow()

    # Calculate the expiration time (15 minutes from now)
    expiration_time = current_time + timedelta(minutes=15)

    # Format the expiration time as a string
    expiration_time_str = expiration_time.strftime('%Y-%m-%dT%H:%M:%SZ')

    return expiration_time_str
