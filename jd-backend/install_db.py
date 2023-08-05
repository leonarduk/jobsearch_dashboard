import boto3

dynamodb = boto3.resource('dynamodb', endpoint_url='http://localhost:8000')


def create_table(table_name, attribute_definitions, key_schema, read_capacity_units, write_capacity_units):
    try:
        table = dynamodb.create_table(
            TableName=table_name,
            AttributeDefinitions=attribute_definitions,
            KeySchema=key_schema,
            ProvisionedThroughput={
                'ReadCapacityUnits': read_capacity_units,
                'WriteCapacityUnits': write_capacity_units
            }
        )
        table.meta.client.get_waiter('table_exists').wait(TableName=table_name)
        print(f"Table '{table_name}' created successfully.")
    except Exception as e:
        print(f"Error creating table '{table_name}': {str(e)}")


if __name__ == '__main__':
    UserTable = {
        "TableName": "JD_User",
        "AttributeDefinitions": [
            {
                "AttributeName": "UserId",
                "AttributeType": "S"
            }
        ],
        "KeySchema": [
            {
                "AttributeName": "UserId",
                "KeyType": "HASH"
            }
        ],
        "ReadCapacityUnits": 5,
        "WriteCapacityUnits": 5
    }

    JobApplicationTable = {
        "TableName": "JD_JobApplication",
        "AttributeDefinitions": [
            {
                "AttributeName": "ApplicationId",
                "AttributeType": "S"
            },
            {
                "AttributeName": "UserId",
                "AttributeType": "S"
            }
        ],
        "KeySchema": [
            {
                "AttributeName": "ApplicationId",
                "KeyType": "HASH"
            },
            {
                "AttributeName": "UserId",
                "KeyType": "RANGE"
            }
        ],
        "ReadCapacityUnits": 5,
        "WriteCapacityUnits": 5
    }

    RecruiterTable = {
        "TableName": "JD_Recruiter",
        "AttributeDefinitions": [
            {
                "AttributeName": "RecruiterId",
                "AttributeType": "S"
            }
        ],
        "KeySchema": [
            {
                "AttributeName": "RecruiterId",
                "KeyType": "HASH"
            }
        ],
        "ReadCapacityUnits": 5,
        "WriteCapacityUnits": 5
    }

    NotesTable = {
        "TableName": "JD_Notes",
        "AttributeDefinitions": [
            {
                "AttributeName": "NoteId",
                "AttributeType": "S"
            },
            {
                "AttributeName": "UserId",
                "AttributeType": "S"
            }
        ],
        "KeySchema": [
            {
                "AttributeName": "NoteId",
                "KeyType": "HASH"
            },
            {
                "AttributeName": "UserId",
                "KeyType": "RANGE"
            }
        ],
        "ReadCapacityUnits": 5,
        "WriteCapacityUnits": 5
    }

    RemindersTable = {
        "TableName": "JD_Reminders",
        "AttributeDefinitions": [
            {
                "AttributeName": "ReminderId",
                "AttributeType": "S"
            },
            {
                "AttributeName": "UserId",
                "AttributeType": "S"
            }
        ],
        "KeySchema": [
            {
                "AttributeName": "ReminderId",
                "KeyType": "HASH"
            },
            {
                "AttributeName": "UserId",
                "KeyType": "RANGE"
            }
        ],
        "ReadCapacityUnits": 5,
        "WriteCapacityUnits": 5
    }

    tables = [UserTable, JobApplicationTable, RecruiterTable, NotesTable, RemindersTable]

    for table in tables:
        create_table(
            table["TableName"],
            table["AttributeDefinitions"],
            table["KeySchema"],
            table["ReadCapacityUnits"],
            table["WriteCapacityUnits"]
        )
