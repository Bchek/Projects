import json
import boto3
import os

def checkIfInstanceAlarmExists(thisInstanceid):
    
    cloudwatchclient = boto3.client('cloudwatch')
    paginator = cloudwatchclient.get_paginator('describe_alarms')
    for response in paginator.paginate():
        for alarm in response['MetricAlarms']:
            if ((alarm['AlarmName']) == thisInstanceid+'StatusCheckFailed'):
                return True
                break
    return False

def lambda_handler(event, context):
    
    cloudwatchclient = boto3.client('cloudwatch')
    thisInstanceID = event['detail']['instance-id']
    if(checkIfInstanceAlarmExists(thisInstanceID)) == True:
        cloudwatchclient.delete_alarms(AlarmNames=[thisInstanceID+'StatusCheckFailed'])
        
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }
