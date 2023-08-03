import json
import boto3
import uuid

dynamodb = boto3.resource('dynamodb')
table_name = 'JobApplicationsTable'
table = dynamodb.Table(table_name)


def lambda_handler(event, context):
    try:
        # Parse request body
        request_body = json.loads(event['body'])
        company = request_body.get('company')
        position = request_body.get('position')
        date_applied = request_body.get('dateApplied')

        # Validate required fields
        if not company or not position or not date_applied:
            return {
                'statusCode': 400,
                'body': json.dumps('Missing required fields')
            }

        # Generate unique ID for the job application
        job_application_id = str(uuid.uuid4())

        # Insert new job app entry into database
        item = {
            'id': job_application_id,
            'company': company,
            'position': position,
            'dateApplied': date_applied
            # Add other fields as needed
        }
        table.put_item(Item=item)

        # Return the created job app object back to client
        return {
            'statusCode': 201,
            'body': json.dumps(item)
        }

    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps('Server error')
        }
