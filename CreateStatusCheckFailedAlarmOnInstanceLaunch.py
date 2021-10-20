import json
import os
import boto3

allalarms = []
def collectAllExistingAlarms():

    client = boto3.client('cloudwatch')
    paginator = client.get_paginator('describe_alarms')

    for response in paginator.paginate():
        for alarm in response['MetricAlarms']:
            allalarms.append(alarm['AlarmName'])


def checkIfInstanceAlarmExists(thisInstanceid):
  
        AlarmName = thisInstanceid+'StatusCheckFailed'
        if(AlarmName in allalarms):
                return True
        return False
                

def lambda_handler(event, context):
    cloudwatchclient = boto3.client('cloudwatch')
    thisInstanceID = event['detail']['instance-id']
    collectAllExistingAlarms()
    print(allalarms)
    if(checkIfInstanceAlarmExists(thisInstanceID)) == False:
        AlarmName = thisInstanceID + 'StatusCheckFailed'
        cloudwatchclient.put_metric_alarm(
        AlarmName=AlarmName,
        ComparisonOperator='GreaterThanOrEqualToThreshold',
        DatapointsToAlarm = 1,
        EvaluationPeriods=1,
        MetricName='StatusCheckFailed',
        Namespace='AWS/EC2',
        Period=60,
        Statistic='Minimum',
        Threshold=1,
        ActionsEnabled=True,
        AlarmDescription='EC2 Status Check Failed',
        AlarmActions=[
          'arn:aws:sns:us-west-2:376123151937:test'
        ],
          
        Dimensions=[
            {
              'Name': 'InstanceId',
              'Value': thisInstanceID
            },
        ],
        )

    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }
