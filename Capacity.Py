import boto3
import botocore

InstanceType='m5.16xlarge'
InstanceTypeAlternative='m5.12xlarge' 
InstancePlatform='SUSE Linux'
AvailabilityZone='us-west-2d'
InstanceCount = 52
EndDate='11/19/2020 05:00'
EndDateType='limited'                          

def checkCapacity(InstanceType, InstancePlatform, AvailabilityZone, InstanceCount, EndDate, EndDateType): 

    ec2 = boto3.client('ec2', region_name='us-west-2')
    response = ec2.create_capacity_reservation(
                            InstanceType=InstanceType,
                            InstancePlatform=InstancePlatform,
                            AvailabilityZone=AvailabilityZone,
                            InstanceCount=InstanceCount,
                            EndDate=EndDate,
                            EndDateType=EndDateType,
                        )
    cr = response['CapacityReservation']
    cr_status = cr['State']
    print (cr_status)
    return cr_status

def main():
    
    
    try:   
        cr_status = checkCapacity(InstanceType, InstancePlatform, AvailabilityZone, InstanceCount, EndDate, EndDateType)
        print(cr_status)
    except botocore.exceptions.ClientError as e:
        cr_status=e.response['Error']['Code']
    
    if not(cr_status == 'active' ):
        cr_status = checkCapacity(InstanceTypeAlternative, InstancePlatform, AvailabilityZone, InstanceCount, EndDate, EndDateType)
        print (cr_status)
    
        connection = boto3.client('emr',region_name='us-west-2')
        instancetype = InstanceTypeAlternative
    
        cluster_id = connection.run_job_flow(Name='test1_emr_job_boto3',LogUri='s3://athenaresultsbchekuri',ReleaseLabel='emr-5.18.0',
            Applications=[
                {
                    'Name': 'Spark'
                },
            ],
            Instances={
                'InstanceGroups': [
                    {
                        'Name': "Master",
                        'Market': 'ON_DEMAND',
                        'InstanceRole': 'MASTER',
                        'InstanceType': instancetype,
                        'InstanceCount': 1,
                    },
                    {
                        'Name': "Slave",
                        'Market': 'ON_DEMAND',
                        'InstanceRole': 'CORE',
                        'InstanceType': instancetype,
                        'InstanceCount': 10,
                    }
                ],
                'Ec2KeyName': 'TestPair',
                'KeepJobFlowAliveWhenNoSteps': True,
                'TerminationProtected': False,
                'Ec2SubnetId': 'subnet-4e58c765',
            },
            Steps=[
                {
                    'Name': 'file-copy-step',   
                            'ActionOnFailure': 'CONTINUE',
                            'HadoopJarStep': {
                                'Jar': 's3://Snapshot-jar-with-dependencies.jar',
                                'Args': ['test.xml', 'emr-test', 'kula-emr-test-2']
                            }
                }
            ],
            VisibleToAllUsers=True,
            JobFlowRole='EMR_EC2_DefaultRole',
            ServiceRole='EMR_DefaultRole',
            Tags=[
                {
                    'Key': 'tag_name_1',
                    'Value': 'tab_value_1',
                },
                {
                    'Key': 'tag_name_2',
                    'Value': 'tag_value_2',
                },
            ],
        )             

if __name__ == "__main__":
    main()