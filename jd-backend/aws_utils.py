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


# Error code to user-friendly message mapping
ERROR_MESSAGES = {
    "DYNAMO_DB_FAILURE": "We encountered a problem accessing our database. Please try again later.",
    "REQUEST_BODY_FAILURE": "Failed to process your request. Please check your input and try again.",
    "RESPONSE_CREATION_FAILURE": "Failed to process your request. Please try again later."
}


def log_and_raise_error(message, error_code=None):
    if error_code and error_code in ERROR_MESSAGES:
        user_message = ERROR_MESSAGES[error_code]
    else:
        user_message = "An unexpected error occurred. Please try again later."

    logger.error(f"{message} - Error code: {error_code}")
    raise CustomException(user_message)


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
        logger.info(f"Item added successfully: {response}")
    except ClientError as e:
        error_code = e.response['Error']['Code']
        logger.error(f"ClientError: {error_code} - {e}")
        if error_code == 'ProvisionedThroughputExceededException':
            log_and_raise_error("Provisioned throughput exceeded.", "DYNAMO_DB_FAILURE")
        elif error_code == 'ConditionalCheckFailedException':
            log_and_raise_error("Conditional check failed.", "DYNAMO_DB_FAILURE")
        elif error_code == 'InternalServerError':
            log_and_raise_error("Internal server error.", "DYNAMO_DB_FAILURE")
        else:
            log_and_raise_error(str(e))


def get_dynamodb_resource():
    # Check if the function is running locally (offline)
    is_offline = os.environ.get('IS_OFFLINE')
    # Set up the DynamoDB resource based on the environment
    if is_offline:
        dynamodb_resource = boto3.resource(
            'dynamodb',
            region_name='localhost',
            endpoint_url='http://localhost:8000'
        )
    else:
        dynamodb_resource = boto3.resource('dynamodb')

    logger.info(str(dynamodb_resource))
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
        log_and_raise_error(f"Failed to get data from body: {e}", "REQUEST_BODY_FAILURE")


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
        log_and_raise_error(f"Failed to create response: {e}", "RESPONSE_CREATION_FAILURE")
