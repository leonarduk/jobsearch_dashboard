import logging
import base64
import json
import chardet
import os
import boto3
from botocore.exceptions import ClientError

# Initialize the logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


# Define a custom exception class for better error handling
class CustomException(Exception):
    pass


def log_and_raise_error(message):
    logger.error(message)
    raise CustomException(message)


def get_dynamo_client():
    try:
        is_offline = os.environ.get('IS_OFFLINE')
        if is_offline:
            dynamodb = boto3.client('dynamodb', endpoint_url='http://localhost:8000')
        else:
            dynamodb = boto3.client('dynamodb')
        return dynamodb
    except Exception as e:
        log_and_raise_error(f"Failed to get DynamoDB client: {e}")


def add_item_to_table(dynamodb_client, table, item):
    try:
        response = dynamodb_client.put_item(
            TableName=table,
            Item=item)
        print("Item added successfully:", response)
    except ClientError as e:
        if e.response['Error']['Code'] == 'ProvisionedThroughputExceededException':
            print("Error: Provisioned throughput exceeded.")
            # todo handle failures better
        elif e.response['Error']['Code'] == 'ConditionalCheckFailedException':
            print("Error: Conditional check failed.")
        elif e.response['Error']['Code'] == 'InternalServerError':
            print("Error: Internal server error.")
        else:
            print("Error:", e)


def get_dynamodb_resource():
    # Check if the function is running locally (offline)
    is_offline = os.environ.get('IS_OFFLINE')
    print(is_offline)
    # Set up the DynamoDB resource based on the environment
    if is_offline:
        dynamodb_resource = boto3.resource(
            'dynamodb',
            region_name='localhost',
            endpoint_url='http://localhost:8000'
        )
    else:
        dynamodb_resource = boto3.resource('dynamodb')

    print(str(dynamodb_resource))
    return dynamodb_resource


def get_data_from_body(event):
    try:
        if "body" in event:
            body = event['body']
            logger.info("body: " + str(body))

            if "isBase64Encoded" in event and event['isBase64Encoded']:
                decoded_data = base64.b64decode(body)
                result = chardet.detect(decoded_data)
                encoding = result['encoding']
                request_body = decoded_data.decode(encoding)
            else:
                request_body = body

            if isinstance(request_body, dict):
                return request_body

            data = json.loads(request_body)
            return data
        else:
            return event
    except Exception as e:
        log_and_raise_error(f"Failed to get data from body: {e}")


def create_response(message, status_code):
    try:
        logger.info(f"{status_code}: {message}")
        response = {
            "statusCode": status_code,
            "headers": {
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Headers": "Content-Type",
                "Access-Control-Allow-Methods": "OPTIONS,POST",
                "Access-Control-Allow-Credentials": True,
            },
            "body": json.dumps({"message": message})
        }
        return response
    except Exception as e:
        log_and_raise_error(f"Failed to create response: {e}")
