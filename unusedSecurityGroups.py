import boto3


ec2client = boto3.client('ec2')
regions = [region['RegionName'] for region in ec2client.describe_regions()['Regions']]

enisgs=[]
def attachedtoENI(region):
    eniclient = boto3.client('ec2', region_name=region)
    enis = eniclient.describe_network_interfaces()

    for i in enis['NetworkInterfaces']:
        for j in i['Groups']:
                enisgs.append(j['GroupId'])

rdssgs = []
def attachedtoRDS(region):
    rdsclient = boto3.client('rds', region_name=region)
    db_instances = rdsclient.describe_db_instances()
    for i in db_instances['DBInstances']:
        for j in i['VpcSecurityGroups']:
            rdssgs.append(j['VpcSecurityGroupId'])

ec2sgs = []
def attachedtoEC2(region):
    ec2client = boto3.client('ec2', region_name=region)
    response = ec2client.describe_instances()
    for i in response['Reservations']:
        for j in i['Instances']:
            for k in j['SecurityGroups']:
                ec2sgs.append(k['GroupId'])

elbsgs = []
def attachedtoELBV2(region):
    ELBclient2 = boto3.client('elbv2', region_name=region)
    elbs = ELBclient2.describe_load_balancers()
    for i in elbs['LoadBalancers']:
        for j in i['SecurityGroups']:
                    elbsgs.append(j)

secgroups = []
for region in regions:
            client = boto3.client('ec2', region_name=region)
            securitygroups = client.describe_security_groups()
            for sg in securitygroups['SecurityGroups']:
                    if(sg['GroupName'] != 'default'):
                        secgroups.append(sg['GroupId'])
            attachedtoENI(region)
            attachedtoRDS(region)
            attachedtoEC2(region)
            attachedtoELBV2(region)

usedgrouplist = elbsgs+rdssgs+ec2sgs+enisgs
unusedgrouplist = []
for sg in secgroups:
        if sg not in usedgrouplist:
            unusedgrouplist.append(sg)
print(unusedgrouplist)
