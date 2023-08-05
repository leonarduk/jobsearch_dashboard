import base64
import json

import chardet
import os
import boto3


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