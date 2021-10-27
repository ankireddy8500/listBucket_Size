import boto3
import json
from botocore.exceptions import ClientError
import os

def lambda_handler(event,context):
    total_size = 0
    Buckets = []
    s3 = boto3.client('s3')
    response = s3.list_buckets()

    for bucket in response['Buckets']:
        Buckets.append(bucket["Name"])

    count_dict = {}
    for name in Buckets:
        buckets = boto3.resource('s3').Bucket(name)
        for object in buckets.objects.all():
            total_size += object.size
            #print(object.size)
        count_dict[name] = total_size/1024/1024
        value = dict(sorted(count_dict.items(), key=lambda x:x[1]))
        total_size=0
    #print(value)
    for i,j in value.items():
        print(i,":",j, "MB")
        #print(name, ":", (total_size/ 1024 / 1024), "MB")
    #total_size=0
    c = dict((k, v) for k, v in value.items() if v >= 1024)
    print(c)
    #default_region = os.environ['AWS_REGION']
    sns = boto3.client("sns", region_name="us-west-2")
    sns.publish(
          TopicArn="",
          Message=json.dumps(c), 
          Subject="Bucket List above 1GB"
        )
