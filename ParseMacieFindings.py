import json
import boto3


sourceBucket = 'maciebharathbucket'
destBucket =   'maciebharath'
s3FilesToQuarantine = []

def lambda_handler(event, context):
    records = event['Records']
    print(records)
    
    for record in records:
        body = json.loads(record["body"])
        s3FileToQuarantine = body["detail"]['resourcesAffected']['s3Object']['key']
        s3FilesToQuarantine.append(s3FileToQuarantine) 
    print (s3FilesToQuarantine)
        
    
    quarantineFile(s3FilesToQuarantine)
    deleteS3File(s3FilesToQuarantine)

    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }


    
def quarantineFile(s3FilesToQuarantine):
     
     s3 = boto3.resource("s3")
     
     for s3file in s3FilesToQuarantine:
     
         copy_source = {
              'Bucket': sourceBucket,
              'Key'   : s3file
         }
         newFileName = 'Q'+s3file
         s3.meta.client.copy(copy_source, destBucket, newFileName)
         
def deleteS3File(s3FilesToQuarantine):
    
    for s3file in s3FilesToQuarantine:
    
        s3 = boto3.client('s3')
        response = s3.delete_object(
        Bucket=sourceBucket,
        Key=s3file
   
        )
         