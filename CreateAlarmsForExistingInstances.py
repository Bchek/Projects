import boto3
import botocore
from awsretry import AWSRetry


@AWSRetry.backoff(tries=10, delay=2, backoff=1.5)
def get_instances():
    allinstances = []
    client = boto3.client('ec2')

    try:
        paginator = client.get_paginator('describe_instances')
        response_iterator = paginator.paginate(Filters=[{'Name': 'instance-state-name', 'Values': ['running']}])
        for response in response_iterator:
            for instance in response['Reservations']:
                for i in instance['Instances']:
                    allinstances.append(i['InstanceId'])
        return allinstances
    except botocore.exceptions.ClientError as e:
        raise


@AWSRetry.backoff(tries=20, delay=3, backoff=1.5, added_exceptions=['ThrottlingException', 'Throttling'])
def createCloudwatchAlarm():
    cloudwatchclient = boto3.client('cloudwatch')
    allinstances = get_instances()
    print(allinstances)
    print(len(allinstances))
    try:
        for instance in allinstances:
            AlarmName = instance + 'StatusCheckFailed'
            cloudwatchclient.put_metric_alarm(
                AlarmName=AlarmName,
                ComparisonOperator='GreaterThanOrEqualToThreshold',
                DatapointsToAlarm=1,
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
                        'Value': instance
                    },
                ],

            )
    except botocore.exceptions.ClientError as err:
        raise


def main():
    createCloudwatchAlarm()


if __name__ == "__main__":
    main()