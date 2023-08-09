import base64
import json

import chardet
import os
import boto3
from botocore.exceptions import ClientError


def get_dynamo_client():
    # Check if the function is running locally (offline)
    is_offline = os.environ.get('IS_OFFLINE')
    print(is_offline)
    # Set up the DynamoDB resource based on the environment
    if is_offline:
        dynamodb = boto3.client('dynamodb', endpoint_url='http://localhost:8000')
    else:
        dynamodb = boto3.client('dynamodb')

    print(str(dynamodb))
    return dynamodb


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
    if "body" in event:
        body = event['body']
        print("body: " + str(body))

        if "isBase64Encoded" in event:
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

    else:
        data = event

    return data


def create_response(message, status_code):
    print(f"{status_code}: {message}")
    response = {
        "statusCode": status_code,
        "headers": {
            "Access-Control-Allow-Origin": "*",  # Allow requests from any domain
            "Access-Control-Allow-Headers": "Content-Type",  # Add any required headers here
            "Access-Control-Allow-Methods": "OPTIONS,POST",  # Add allowed HTTP methods here
            "Access-Control-Allow-Credentials": True,  # Allow sending of cookies
        },
        "body": json.dumps({"message": message})
    }
    return response
