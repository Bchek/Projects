import json
import string
import boto3
import json
import datetime
from datetime import datetime, timedelta, timezone
import time

def lambda_handler(event, context):
    

    
    client=boto3.client('macie2', 'us-west-2')
    current_datetime = datetime.now()
    jobname = 'MacieJob'+str(current_datetime)
    old_datetime = current_datetime - timedelta(minutes = 15)
    old_datetime = old_datetime.isoformat()
    old_datetime = old_datetime [:-3]
    old_datetime = old_datetime + 'Z'
    
    #sqsclient = boto3.client('sqs', 'us-west-2')
    #response = sqsclient.purge_queue(QueueUrl = 'https://sqs.us-west-2.amazonaws.com/811791950107/MySQSQueue' )
    #print(response)
    
    response1 = response = client.create_classification_job(
    customDataIdentifierIds=[
        '53bf2596-fa63-4bfe-95c4-88a3a8197523',
    ],
    description='MacieJob',
    initialRun=True,
    jobType='ONE_TIME',
    name=jobname,
    s3JobDefinition={
        'bucketDefinitions': [
            {
                'accountId': '811791950107',
                'buckets': [
                    'maciebharathbucket',
                ]
            },
        ],
        'scoping': {
            'excludes': {
                'and': [
                    {
                        'simpleScopeTerm': {
                            'comparator': 'LT',
                            'key': 'OBJECT_LAST_MODIFIED_DATE',
                            'values': [
                                old_datetime,
                            ]
                        },
                    },
                ]
            },
        }
    },
    )

    print(response1)    
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }
