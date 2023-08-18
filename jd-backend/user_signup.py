import logging
from aws_utils import get_data_from_body, get_dynamo_client, create_response, log_and_raise_error, add_item_to_table

# Initialize the logger
logger = logging.getLogger(__name__)

table_name = 'JD_User'

def signup(event, context):
    try:
        data = get_data_from_body(event)

        logger.info(f"Data: {data}")

        # Validate input
        name = data.get('name')
        email = data.get('email')
        password = data.get('password')

        if not name or not email or not password:
            log_and_raise_error("Name, email, and password are required.", "SIGNUP_VALIDATION_FAILURE")

        dynamodb = get_dynamo_client()
        dynamodb.get_waiter('table_exists').wait(TableName=table_name)

        # Check if user already exists
        response = dynamodb.get_item(
            TableName=table_name,
            Key={'UserId': {'S': email}}
        )

        if 'Item' in response:
            log_and_raise_error("User with this email already exists.", "USER_ALREADY_EXISTS")

        # Hash the password
        #    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

        # Perform the put_item operation using the client
        add_item_to_table(dynamodb_client=dynamodb, table=table_name, item={
            'UserId': {'S': email},
            'Email': {'S': email},
            'Name': {'S': name},
            'Password': {'S': password}  # Ideally, you should hash the password before storing
        })

        return create_response("User created successfully.", 200)

    except Exception as e:
        logger.error(f"Error during signup: {e}")
        log_and_raise_error(f"An error occurred during sign up: {e}", "SIGNUP_ERROR")
