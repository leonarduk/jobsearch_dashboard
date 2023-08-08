import json
import bcrypt
import secrets

from aws_utils import get_data_from_body, get_dynamo_client, create_response, add_item_to_table


def login(event, context):
    # print(event)
    data = get_data_from_body(event)

    print("Data" + str(data))

    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return create_response("Username and password are required.", 400)

    user_table = "JD_User"
    dynamodb_client = get_dynamo_client()
    dynamodb_client.get_waiter('table_exists').wait(TableName=user_table)

    # Check if db_user already exists
    response = dynamodb_client.get_item(
        TableName=user_table,
        Key={'UserId': {'S': username}}
    )

    if 'Item' not in response:
        return create_response("Invalid username or password.", 401)

    db_user = response['Item']
    print(f"db_user {db_user}")
    stored_password_hash = db_user['Password']['S']

    # Validate password
    # if not bcrypt.checkpw(password.encode('utf-8'), stored_password_hash.encode('utf-8')):
    if stored_password_hash != password:
        return create_response("Invalid username or password.", 401)

    # Generate session ID (you can use any secure random string generator)
    # In a production setting, consider using UUID or other secure session ID generators.
    session_id = generate_session_id()

    # Save session ID to the JD_Sessions table with an expiration time (e.g., 15 minutes)
    session_table = "JD_Sessions"
    dynamodb_client = get_dynamo_client()
    dynamodb_client.get_waiter('table_exists').wait(TableName=session_table)

    print(dynamodb_client)
    table = dynamodb_client.Table(session_table)
    add_item_to_table(table=table,
                      Item={'session_id': session_id, 'user_id': db_user['user_id'], 'expiration': get_expiration_time()})

    # Return the session ID to the client
    print(f"Logged in")
    return {
        "statusCode": 200,
        "body": json.dumps({"session_id": session_id})
    }


def generate_session_id():
    # Generate a secure random session ID using the secrets module
    # In a production setting, consider using UUID or other secure session ID generators.
    return secrets.token_hex(16)  # Generate a random 32-character hexadecimal string


def get_expiration_time():
    # Implement your logic to calculate the expiration time for the session (e.g., 15 minutes from now).
    pass
