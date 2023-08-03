import json
import boto3

dynamodb = boto3.resource('dynamodb')
table_name = 'JobApplicationsTable'
table = dynamodb.Table(table_name)


def lambda_handler(event, context):
    try:
        job_application_id = event['pathParameters']['id']

        # Lookup job app by ID in database
        response = table.get_item(Key={'id': job_application_id})
        item = response.get('Item')

        if not item:
            return {
                'statusCode': 404,
                'body': json.dumps('Job application not found')
            }

        # Return job app data object back to client
        return {
            'statusCode': 200,
            'body': json.dumps(item)
        }

    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps('Server error')
        }
