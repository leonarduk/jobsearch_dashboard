from aws_utils import get_data_from_body, get_dynamo_client, create_response, add_item_to_table


table_name = 'JD_User'


def signup(event, context):
    try:
        data = get_data_from_body(event)

        print("Data" + str(data))

        # Validate input
        name = data.get('name')
        email = data.get('email')
        password = data.get('password')

        if not name or not email or not password:
            return create_response("Name, email, and password are required.", 400)

        dynamodb = get_dynamo_client()
        dynamodb.get_waiter('table_exists').wait(TableName=table_name)

        # Check if user already exists
        # Perform the get_item operation using the client
        response = dynamodb.get_item(
            TableName=table_name,
            Key={'UserId': {'S': email}}
        )

        if 'Item' in response:
            return create_response("User with this email already exists.", 409)

        # Hash the password
        #    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

        # Perform the put_item operation using the client
        add_item_to_table(dynamodb_client=dynamodb, table=table_name, item={
            'UserId': {'S': email},
            'Email': {'S': email},
            'Name': {'S': name},
            'Password': {'S': password}
        })

        # Return response
        response = create_response("User created successfully.", 200)

        return response

    except Exception as e:
        print("Error" + str(e))
        # Handle any exceptions and return an error response
        response = create_response(f"An error occurred during sign up.{e}", 500)
        return response


